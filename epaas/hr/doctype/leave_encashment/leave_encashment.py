# -*- coding: utf-8 -*-
# Copyright (c) 2018, Dataent Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import dataent
from dataent import _
from dataent.model.document import Document
from dataent.utils import getdate, nowdate, flt
from epaas.hr.utils import set_employee_name
from epaas.hr.doctype.leave_application.leave_application import get_leave_balance_on
from epaas.hr.doctype.salary_structure_assignment.salary_structure_assignment import get_assigned_salary_structure

class LeaveEncashment(Document):
	def validate(self):
		set_employee_name(self)
		self.get_leave_details_for_encashment()

		if not self.encashment_date:
			self.encashment_date = getdate(nowdate())

	def before_submit(self):
		if self.encashment_amount <= 0:
			dataent.throw(_("You can only submit Leave Encashment for a valid encashment amount"))

	def on_submit(self):
		if not self.leave_allocation:
			self.leave_allocation = self.get_leave_allocation()
		additional_salary = dataent.new_doc("Additional Salary")
		additional_salary.company = dataent.get_value("Employee", self.employee, "company")
		additional_salary.employee = self.employee
		additional_salary.salary_component = dataent.get_value("Leave Type", self.leave_type, "earning_component")
		additional_salary.payroll_date = self.encashment_date
		additional_salary.amount = self.encashment_amount
		additional_salary.submit()

		self.db_set("additional_salary", additional_salary.name)

		# Set encashed leaves in Allocation
		dataent.db.set_value("Leave Allocation", self.leave_allocation, "total_leaves_encashed",
				dataent.db.get_value('Leave Allocation', self.leave_allocation, 'total_leaves_encashed') + self.encashable_days)

	def on_cancel(self):
		if self.additional_salary:
			dataent.get_doc("Additional Salary", self.additional_salary).cancel()
			self.db_set("additional_salary", "")

		if self.leave_allocation:
			dataent.db.set_value("Leave Allocation", self.leave_allocation, "total_leaves_encashed",
				dataent.db.get_value('Leave Allocation', self.leave_allocation, 'total_leaves_encashed') - self.encashable_days)

	def get_leave_details_for_encashment(self):
		salary_structure = get_assigned_salary_structure(self.employee, self.encashment_date or getdate(nowdate()))
		if not salary_structure:
			dataent.throw(_("No Salary Structure assigned for Employee {0} on given date {1}").format(self.employee, self.encashment_date))

		if not dataent.db.get_value("Leave Type", self.leave_type, 'allow_encashment'):
			dataent.throw(_("Leave Type {0} is not encashable").format(self.leave_type))

		self.leave_balance = get_leave_balance_on(self.employee, self.leave_type,
			self.encashment_date or getdate(nowdate()), consider_all_leaves_in_the_allocation_period=True)

		encashable_days = self.leave_balance - dataent.db.get_value('Leave Type', self.leave_type, 'encashment_threshold_days')
		self.encashable_days = encashable_days if encashable_days > 0 else 0

		per_day_encashment = dataent.db.get_value('Salary Structure', salary_structure , 'leave_encashment_amount_per_day')
		self.encashment_amount = self.encashable_days * per_day_encashment if per_day_encashment > 0 else 0

		self.leave_allocation = self.get_leave_allocation()
		return True

	def get_leave_allocation(self):
		leave_allocation = dataent.db.sql("""select name from `tabLeave Allocation` where '{0}'
		between from_date and to_date and docstatus=1 and leave_type='{1}'
		and employee= '{2}'""".format(self.encashment_date or getdate(nowdate()), self.leave_type, self.employee))

		return leave_allocation[0][0] if leave_allocation else None
