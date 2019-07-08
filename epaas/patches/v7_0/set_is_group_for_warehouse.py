from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doc("stock", "doctype", "warehouse")
	dataent.db.sql("""update tabWarehouse
		set is_group = if ((ifnull(is_group, "No") = "Yes" or ifnull(is_group, 0) = 1), 1, 0)""")