from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doc("stock", "doctype", "bin")
	bins = dataent.db.sql("select name from `tabBin` where reserved_qty_for_production > 0")
	for d in bins:
		bin_doc = dataent.get_doc("Bin", d[0])
		bin_doc.update_reserved_qty_for_production()
