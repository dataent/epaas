from __future__ import unicode_literals
import dataent

from dataent.model.utils.rename_field import rename_field

def execute():
	""" 
		Rename Total Margin field to Rate With Margin in
		"Sales Order Item", "Sales Invoice Item", "Delivery Note Item",
		"Quotation Item"
	"""

	for d in ("Sales Order Item", "Sales Invoice Item",
		"Delivery Note Item", "Quotation Item"):
		dataent.reload_doctype(d)
		rename_field_if_exists(d, "total_margin", "rate_with_margin")


def rename_field_if_exists(doctype, old_fieldname, new_fieldname):
	try:
		rename_field(doctype, old_fieldname, new_fieldname)
	except Exception as e:
		if e.args[0] != 1054:
			raise
