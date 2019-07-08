from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doctype('Sales Order')
	dataent.reload_doctype('Sales Invoice')
	dataent.reload_doctype('Quotation')
	dataent.reload_doctype('Delivery Note')

	doctype_list = ['Sales Order Item', 'Delivery Note Item', 'Quotation Item', 'Sales Invoice Item']

	for doctype in doctype_list:
		dataent.reload_doctype(doctype)
		dataent.db.sql("""update `tab{doctype}` 
		 		set uom = stock_uom, conversion_factor = 1, stock_qty = qty""".format(doctype=doctype))