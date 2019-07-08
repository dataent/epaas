# Copyright (c) 2017, Dataent and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent
from dataent.utils.nestedset import rebuild_tree

def execute():
	dataent.reload_doc('assets', 'doctype', 'asset_finance_book')
	dataent.reload_doc('assets', 'doctype', 'depreciation_schedule')
	dataent.reload_doc('assets', 'doctype', 'asset_category')
	dataent.reload_doc('assets', 'doctype', 'asset')
	dataent.reload_doc('assets', 'doctype', 'asset_movement')
	dataent.reload_doc('assets', 'doctype', 'asset_category_account')

	if dataent.db.has_column("Asset", "warehouse"):
		dataent.db.sql(""" update `tabAsset` ast, `tabWarehouse` wh
			set ast.location = wh.warehouse_name where ast.warehouse = wh.name""")

		dataent.db.sql(""" update `tabAsset Movement` ast_mv
			set ast_mv.source_location = (select warehouse_name from `tabWarehouse` where name = ast_mv.source_warehouse),
			ast_mv.target_location = (select warehouse_name from `tabWarehouse` where name = ast_mv.target_warehouse)""")

		for d in dataent.get_all('Asset'):
			doc = dataent.get_doc('Asset', d.name)
			if doc.calculate_depreciation:
				fb = doc.append('finance_books', {
					'depreciation_method': doc.depreciation_method,
					'total_number_of_depreciations': doc.total_number_of_depreciations,
					'frequency_of_depreciation': doc.frequency_of_depreciation,
					'depreciation_start_date': doc.next_depreciation_date,
					'expected_value_after_useful_life': doc.expected_value_after_useful_life,
					'value_after_depreciation': doc.value_after_depreciation
				})

				fb.db_update()

		dataent.db.sql(""" update `tabDepreciation Schedule` ds, `tabAsset` ast
			set ds.depreciation_method = ast.depreciation_method, ds.finance_book_id = 1 where ds.parent = ast.name """)

		for category in dataent.get_all('Asset Category'):
			asset_category_doc = dataent.get_doc("Asset Category", category)
			row = asset_category_doc.append('finance_books', {
				'depreciation_method': asset_category_doc.depreciation_method,
				'total_number_of_depreciations': asset_category_doc.total_number_of_depreciations,
				'frequency_of_depreciation': asset_category_doc.frequency_of_depreciation
			})

			row.db_update()