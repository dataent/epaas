from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doc("projects", "doctype", "project")

	dataent.db.sql("""
		update `tabProject` p
		set total_sales_amount = ifnull((select sum(base_grand_total)
			from `tabSales Order` where project=p.name and docstatus=1), 0)
	""")