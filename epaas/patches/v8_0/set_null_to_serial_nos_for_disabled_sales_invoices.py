# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent
from epaas.stock.stock_balance import update_bin_qty, get_reserved_qty

def execute():
	dataent.db.sql("""
		update 
			`tabSales Invoice Item` 
		set serial_no = NULL
		where 
			parent in (select name from `tabSales Invoice` where update_stock = 0 and docstatus = 1)""")