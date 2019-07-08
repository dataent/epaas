from __future__ import unicode_literals

import dataent

def execute():
	dataent.db.sql("""Update `tabItem` as item set default_bom = NULL where 
		not exists(select name from `tabBOM` as bom where item.default_bom = bom.name and bom.docstatus =1 )""")