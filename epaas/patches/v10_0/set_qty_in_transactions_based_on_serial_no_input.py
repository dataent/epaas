# Copyright (c) 2017, Dataent and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doc("stock", "doctype", "stock_settings")

	ss = dataent.get_doc("Stock Settings")
	ss.set_qty_in_transactions_based_on_serial_no_input = 1

	if ss.default_warehouse \
		and not dataent.db.exists("Warehouse", ss.default_warehouse):
			ss.default_warehouse = None

	if ss.stock_uom and not dataent.db.exists("UOM", ss.stock_uom):
		ss.stock_uom = None

	ss.flags.ignore_mandatory = True
	ss.save()