from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doc('accounts', 'doctype', 'sales_invoice')
	dataent.db.sql("""update `tabSales Invoice` set from_date = invoice_period_from_date,
		to_date = invoice_period_to_date, is_recurring = convert_into_recurring_invoice""")
