# Copyright (c) 2017, Dataent and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals

import dataent


def execute():
	dataent.reload_doc("stock", "doctype", "item_barcode")
	if dataent.get_all("Item Barcode", limit=1): return
	if "barcode" not in dataent.db.get_table_columns("Item"): return

	items_barcode = dataent.db.sql("select name, barcode from tabItem where barcode is not null", as_dict=True)
	dataent.reload_doc("stock", "doctype", "item")



	for item in items_barcode:
		barcode = item.barcode.strip()

		if barcode and '<' not in barcode:
			try:
				dataent.get_doc({
					'idx': 0,
					'doctype': 'Item Barcode',
					'barcode': barcode,
					'parenttype': 'Item',
					'parent': item.name,
					'parentfield': 'barcodes'
				}).insert()
			except (dataent.DuplicateEntryError, dataent.UniqueValidationError):
				continue
