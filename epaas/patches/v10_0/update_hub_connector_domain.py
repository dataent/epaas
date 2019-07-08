from __future__ import unicode_literals
import dataent

def execute():
	if dataent.db.table_exists("Data Migration Connector"):
		dataent.db.sql("""
			UPDATE `tabData Migration Connector`
			SET hostname = 'https://hubmarket.org'
			WHERE connector_name = 'Hub Connector'
		""")