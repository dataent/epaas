# -*- coding: utf-8 -*-
# Copyright (c) 2018, Dataent Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import dataent
from dataent.model.document import Document
from dataent import _
from dataent.utils import getdate, date_diff

class AdditionalSalary(Document):
	def before_insert(self):
		if dataent.db.exists("Additional Salary", {"employee": self.employee, "salary_component": self.salary_component,
			"amount": self.amount, "payroll_date": self.payroll_date, "company": self.company}):

			dataent.throw(_("Additional Salary Component Exists."))

	def validate(self):
		self.validate_dates()
		if self.amount < 0:
			dataent.throw(_("Amount should not be less than zero."))

	def validate_dates(self):
 		date_of_joining, relieving_date = dataent.db.get_value("Employee", self.employee,
			["date_of_joining", "relieving_date"])
 		if date_of_joining and getdate(self.payroll_date) < getdate(date_of_joining):
 			dataent.throw(_("Payroll date can not be less than employee's joining date"))

	def get_amount(self, sal_start_date, sal_end_date):
		start_date = getdate(sal_start_date)
		end_date = getdate(sal_end_date)
		total_days = date_diff(getdate(self.to_date), getdate(self.from_date)) + 1
		amount_per_day = self.amount / total_days
		if getdate(sal_start_date) <= getdate(self.from_date):
			start_date = getdate(self.from_date)
		if getdate(sal_end_date) > getdate(self.to_date):
			end_date = getdate(self.to_date)
		no_of_days = date_diff(getdate(end_date), getdate(start_date)) + 1
		return amount_per_day * no_of_days

@dataent.whitelist()
def get_additional_salary_component(employee, start_date, end_date):
	additional_components = dataent.db.sql("""
		select salary_component, sum(amount) as amount, overwrite_salary_structure_amount, deduct_full_tax_on_selected_payroll_date
		from `tabAdditional Salary`
		where employee=%(employee)s
			and docstatus = 1
			and payroll_date between %(from_date)s and %(to_date)s
		group by salary_component, overwrite_salary_structure_amount
		order by salary_component, overwrite_salary_structure_amount
	""", {
		'employee': employee,
		'from_date': start_date,
		'to_date': end_date
	}, as_dict=1)

	additional_components_list = []
	component_fields = ["depends_on_payment_days", "salary_component_abbr", "is_tax_applicable", "variable_based_on_taxable_salary", 'type']
	for d in additional_components:
		struct_row = dataent._dict({'salary_component': d.salary_component})
		component = dataent.get_all("Salary Component", filters={'name': d.salary_component}, fields=component_fields)
		if component:
			struct_row.update(component[0])

		struct_row['deduct_full_tax_on_selected_payroll_date'] = d.deduct_full_tax_on_selected_payroll_date
		struct_row['is_additional_component'] = 1

		additional_components_list.append(dataent._dict({
			'amount': d.amount,
			'type': component[0].type,
			'struct_row': struct_row,
			'overwrite': d.overwrite_salary_structure_amount,
		}))
	return additional_components_list