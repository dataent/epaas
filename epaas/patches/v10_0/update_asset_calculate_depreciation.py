from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doc('assets', 'doctype', 'asset')
	dataent.reload_doc('assets', 'doctype', 'depreciation_schedule')

	dataent.db.sql("""
		update tabAsset a
		set calculate_depreciation = 1
		where exists(select ds.name from `tabDepreciation Schedule` ds where ds.parent=a.name)
	""")