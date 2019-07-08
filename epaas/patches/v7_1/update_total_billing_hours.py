from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doc('projects', 'doctype', 'timesheet_detail')
	dataent.reload_doc('accounts', 'doctype', 'sales_invoice_timesheet')

	dataent.db.sql("""update tabTimesheet set total_billable_hours=total_hours 
		where total_billable_amount>0 and docstatus = 1""")

	dataent.db.sql("""update `tabTimesheet Detail` set billing_hours=hours where docstatus < 2""")

	dataent.db.sql(""" update `tabSales Invoice Timesheet` set billing_hours = (select total_billable_hours from `tabTimesheet`
		where name = time_sheet) where time_sheet is not null""")