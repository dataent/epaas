from __future__ import unicode_literals
import dataent

def execute():
	default_warehouse = dataent.db.get_value("Stock Settings", None, "default_warehouse")
	if default_warehouse:
		if not dataent.db.get_value("Warehouse", {"name": default_warehouse}):
			dataent.db.set_value("Stock Settings", None, "default_warehouse", "")