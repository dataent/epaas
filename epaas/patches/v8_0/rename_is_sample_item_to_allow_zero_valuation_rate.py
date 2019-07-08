from __future__ import unicode_literals
import dataent
from dataent.model.utils.rename_field import rename_field

def execute():
	
	doc_list = ["Purchase Invoice Item", "Stock Entry Detail", "Delivery Note Item", 
		"Purchase Receipt Item", "Sales Invoice Item"]
	
	for doctype in doc_list:
		dataent.reload_doctype(doctype)
		if "is_sample_item" in dataent.db.get_table_columns(doctype):
			rename_field(doctype, "is_sample_item", "allow_zero_valuation_rate")