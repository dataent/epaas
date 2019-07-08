# Copyright (c) 2017, Dataent and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doctype("Warehouse")
	dataent.db.sql("""
		update 
			`tabWarehouse` 
		set 
			account = (select name from `tabAccount` 
				where account_type = 'Stock' and 
				warehouse = `tabWarehouse`.name and is_group = 0 limit 1)""")