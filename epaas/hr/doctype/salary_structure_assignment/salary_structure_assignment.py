# -*- coding: utf-8 -*-
# Copyright (c) 2018, Dataent Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import dataent
from dataent import _
from dataent.utils import getdate
from dataent.model.document import Document

class DuplicateAssignment(dataent.ValidationError): pass

class SalaryStructureAssignment(Document):
	def validate(self):
		self.validate_dates()

	def validate_dates(self):
		joining_date, relieving_date = dataent.db.get_value("Employee", self.employee,
			["date_of_joining", "relieving_date"])

		if self.from_date:
			if dataent.db.exists("Salary Structure Assignment", {"employee": self.employee, "from_date": self.from_date, "docstatus": 1}):
				dataent.throw(_("Salary Structure Assignment for Employee already exists"), DuplicateAssignment)

			if joining_date and getdate(self.from_date) < joining_date:
				dataent.throw(_("From Date {0} cannot be before employee's joining Date {1}")
					.format(self.from_date, joining_date))

			# flag - old_employee is for migrating the old employees data via patch
			if relieving_date and getdate(self.from_date) > relieving_date and not self.flags.old_employee:
				dataent.throw(_("From Date {0} cannot be after employee's relieving Date {1}")
					.format(self.from_date, relieving_date))

def get_assigned_salary_structure(employee, on_date):
	if not employee or not on_date:
		return None
	salary_structure = dataent.db.sql("""
		select salary_structure from `tabSalary Structure Assignment`
		where employee=%(employee)s
		and docstatus = 1
		and %(on_date)s >= from_date order by from_date desc limit 1""", {
			'employee': employee,
			'on_date': on_date,
		})
	return salary_structure[0][0] if salary_structure else None
