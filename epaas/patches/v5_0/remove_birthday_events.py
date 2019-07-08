from __future__ import unicode_literals
import dataent

def execute():
	for e in dataent.db.sql_list("""select name from tabEvent where
		repeat_on='Every Year' and ref_type='Employee'"""):
		dataent.delete_doc("Event", e, force=True)
