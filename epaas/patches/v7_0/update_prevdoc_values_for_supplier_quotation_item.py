from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doctype('Supplier Quotation Item')
	for data in dataent.db.sql(""" select prevdoc_docname, prevdoc_detail_docname, name
		from `tabSupplier Quotation Item` where prevdoc_docname is not null""", as_dict=True):
		dataent.db.set_value("Supplier Quotation Item", data.name, "material_request", data.prevdoc_docname)
		dataent.db.set_value("Supplier Quotation Item", data.name, "material_request_item", data.prevdoc_detail_docname)