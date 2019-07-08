from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doc('stock', 'doctype', 'item')
	dataent.db.sql("""update `tabItem` set publish_in_hub = 0""")
