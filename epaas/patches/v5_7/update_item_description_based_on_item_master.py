from __future__ import unicode_literals
import dataent

def execute():
	name = dataent.db.sql(""" select name from `tabPatch Log` \
		where \
			patch like 'execute:dataent.db.sql("update `tabProduction Order` pro set description%' """)
	if not name:
		dataent.db.sql("update `tabProduction Order` pro \
			set \
				description = (select description from tabItem where name=pro.production_item) \
			where \
				ifnull(description, '') = ''")
