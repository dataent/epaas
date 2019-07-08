from __future__ import unicode_literals
import dataent
from epaas.regional.india.setup import make_custom_fields
from epaas.controllers.taxes_and_totals import get_itemised_tax_breakup_html

def execute():
	companies = [d.name for d in dataent.get_all('Company', filters = {'country': 'India'})]
	if not companies:
		return

	make_custom_fields()

	# update invoice copy value
	values = ["Original for Recipient", "Duplicate for Transporter",
		"Duplicate for Supplier", "Triplicate for Supplier"]
	for d in values:
		dataent.db.sql("update `tabSales Invoice` set invoice_copy=%s where invoice_copy=%s", (d, d))

	# update tax breakup in transactions made after 1st July 2017
	doctypes = ["Quotation", "Sales Order", "Delivery Note", "Sales Invoice", 
		"Supplier Quotation", "Purchase Order", "Purchase Receipt", "Purchase Invoice"]

	for doctype in doctypes:
		dataent.reload_doctype(doctype)

		date_field = "posting_date"
		if doctype in ["Quotation", "Sales Order", "Supplier Quotation", "Purchase Order"]:
			date_field = "transaction_date"

		records = [d.name for d in dataent.get_all(doctype, filters={
			"docstatus": ["!=", 2],
			date_field: [">=", "2017-07-01"],
			"company": ["in", companies],
			"total_taxes_and_charges": [">", 0],
			"other_charges_calculation": ""
		})]
		if records:
			dataent.db.sql("""
				update `tab%s Item` dt_item
				set gst_hsn_code = (select gst_hsn_code from tabItem where name=dt_item.item_code)
				where parent in (%s)
					and (gst_hsn_code is null or gst_hsn_code = '')
			""" % (doctype, ', '.join(['%s']*len(records))), tuple(records))

			for record in records:
				doc = dataent.get_doc(doctype, record)
				html = get_itemised_tax_breakup_html(doc)
				doc.db_set("other_charges_calculation", html, update_modified=False)