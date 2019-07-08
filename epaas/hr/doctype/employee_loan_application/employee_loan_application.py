# -*- coding: utf-8 -*-
# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import dataent, math
from dataent import _
from dataent.utils import flt, rounded
from dataent.model.mapper import get_mapped_doc
from dataent.model.document import Document

from epaas.hr.doctype.employee_loan.employee_loan import get_monthly_repayment_amount, check_repayment_method

class EmployeeLoanApplication(Document):
	def validate(self):
		check_repayment_method(self.repayment_method, self.loan_amount, self.repayment_amount, self.repayment_periods)
		self.validate_loan_amount()
		self.get_repayment_details()

	def validate_loan_amount(self):
		maximum_loan_limit = dataent.db.get_value('Loan Type', self.loan_type, 'maximum_loan_amount')
		if maximum_loan_limit and self.loan_amount > maximum_loan_limit:
			dataent.throw(_("Loan Amount cannot exceed Maximum Loan Amount of {0}").format(maximum_loan_limit))

	def get_repayment_details(self):
		if self.repayment_method == "Repay Over Number of Periods":
			self.repayment_amount = get_monthly_repayment_amount(self.repayment_method, self.loan_amount, self.rate_of_interest, self.repayment_periods)

		if self.repayment_method == "Repay Fixed Amount per Period":
			monthly_interest_rate = flt(self.rate_of_interest) / (12 *100)
			if monthly_interest_rate:
				monthly_interest_amount = self.loan_amount * monthly_interest_rate
				if monthly_interest_amount >= self.repayment_amount:
					dataent.throw(_("Repayment amount {} should be greater than monthly interest amount {}").
						format(self.repayment_amount, monthly_interest_amount))

				self.repayment_periods = math.ceil((math.log(self.repayment_amount) - 
					math.log(self.repayment_amount - (monthly_interest_amount))) /
					(math.log(1 + monthly_interest_rate)))
			else:
				self.repayment_periods = self.loan_amount / self.repayment_amount

		self.calculate_payable_amount()
		
	def calculate_payable_amount(self):
		balance_amount = self.loan_amount
		self.total_payable_amount = 0
		self.total_payable_interest = 0

		while(balance_amount > 0):
			interest_amount = rounded(balance_amount * flt(self.rate_of_interest) / (12*100))
			balance_amount = rounded(balance_amount + interest_amount - self.repayment_amount)

			self.total_payable_interest += interest_amount
			
		self.total_payable_amount = self.loan_amount + self.total_payable_interest
		
@dataent.whitelist()
def make_employee_loan(source_name, target_doc = None):
	doclist = get_mapped_doc("Employee Loan Application", source_name, {
		"Employee Loan Application": {
			"doctype": "Employee Loan",
			"validation": {
				"docstatus": ["=", 1]
			}
		}
	}, target_doc)

	return doclist