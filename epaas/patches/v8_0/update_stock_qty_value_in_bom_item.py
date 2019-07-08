# Copyright (c) 2017, Dataent and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doc('manufacturing', 'doctype', 'bom_item')
	dataent.reload_doc('manufacturing', 'doctype', 'bom_explosion_item')
	dataent.reload_doc('manufacturing', 'doctype', 'bom_scrap_item')
	dataent.db.sql("update `tabBOM Item` set stock_qty = qty, uom = stock_uom, conversion_factor = 1")
	dataent.db.sql("update `tabBOM Explosion Item` set stock_qty = qty")
	if "qty" in dataent.db.get_table_columns("BOM Scrap Item"):
		dataent.db.sql("update `tabBOM Scrap Item` set stock_qty = qty")