from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doc('accounts', 'doctype', 'sales_invoice')
	dataent.reload_doc('accounts', 'doctype', 'sales_invoice_payment')
	for time_sheet in dataent.db.sql(""" select sales_invoice, name, total_billable_amount from `tabTimesheet`
		where sales_invoice is not null and docstatus < 2""", as_dict=True):
		if not dataent.db.exists('Sales Invoice', time_sheet.sales_invoice):
			continue
		si_doc = dataent.get_doc('Sales Invoice', time_sheet.sales_invoice)
		ts = si_doc.append('timesheets',{})
		ts.time_sheet = time_sheet.name
		ts.billing_amount = time_sheet.total_billable_amount
		ts.db_update()
		si_doc.calculate_billing_amount_from_timesheet()
		si_doc.db_set("total_billing_amount", si_doc.total_billing_amount, update_modified = False)