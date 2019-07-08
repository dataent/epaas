from __future__ import unicode_literals
import dataent

def execute():
	for doctype, fieldname in (
		("Sales Order", "per_billed"),
		("Sales Order", "per_delivered"),
		("Delivery Note", "per_installed"),
		("Purchase Order", "per_billed"),
		("Purchase Order", "per_received"),
		("Material Request", "per_ordered"),
	):
		dataent.db.sql("""update `tab{doctype}` set `{fieldname}`=round(`{fieldname}`, 2)""".format(
			doctype=doctype, fieldname=fieldname))
