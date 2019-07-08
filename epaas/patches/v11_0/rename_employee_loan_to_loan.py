from __future__ import unicode_literals
import dataent
from dataent.model.utils.rename_field import rename_field

def execute():
	if dataent.db.table_exists("Employee Loan Application") and not dataent.db.table_exists("Loan Application"):
		dataent.rename_doc("DocType", "Employee Loan Application", "Loan Application", force=True)

	if dataent.db.table_exists("Employee Loan") and not dataent.db.table_exists("Loan"):
		dataent.rename_doc("DocType", "Employee Loan", "Loan", force=True)

	dataent.reload_doc("hr", "doctype", "loan_application")
	dataent.reload_doc("hr", "doctype", "loan")
	dataent.reload_doc("hr", "doctype", "salary_slip_loan")

	for doctype in ['Loan', 'Salary Slip Loan']:
		if dataent.db.has_column(doctype, 'employee_loan_account'):
			rename_field(doctype, "employee_loan_account", "loan_account")

	columns = {'employee': 'applicant', 'employee_name': 'applicant_name'}
	for doctype in ['Loan Application', 'Loan']:
		dataent.db.sql(""" update `tab{doctype}` set applicant_type = 'Employee' """
			.format(doctype=doctype))
		for column, new_column in columns.items():
			if dataent.db.has_column(doctype, column):
				rename_field(doctype, column, new_column)

		dataent.delete_doc('DocType', doctype)