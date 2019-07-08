from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doctype("GL Entry")
	
	for doctype in ("Delivery Note", "Sales Invoice", "Stock Entry"):
		dataent.db.sql("""
			update `tabGL Entry` gle, `tab{0}` dt
			set gle.project = dt.project
			where gle.voucher_type=%s and gle.voucher_no = dt.name
				and ifnull(gle.cost_center, '') != '' and ifnull(dt.project, '') != ''
		""".format(doctype), doctype)
		
	for doctype in ("Purchase Receipt", "Purchase Invoice"):
		dataent.db.sql("""
			update `tabGL Entry` gle, `tab{0} Item` dt
			set gle.project = dt.project
			where gle.voucher_type=%s and gle.voucher_no = dt.parent and gle.cost_center=dt.cost_center 
				and ifnull(gle.cost_center, '') != '' and ifnull(dt.project, '') != ''
		""".format(doctype), doctype)