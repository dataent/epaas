from __future__ import unicode_literals
import dataent

def execute():
	for data in dataent.get_all('Sales Order', fields = ["name"], filters = [["docstatus", "=", "1"], ["grand_total", "=", "0"]]):
		sales_order = dataent.get_doc('Sales Order', data.name)
		sales_order.set_status(update=True, update_modified = False)