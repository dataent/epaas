from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doctype("Project")
	
	dataent.db.sql('''
		UPDATE `tabProject`
		SET copied_from=name
		WHERE copied_from is NULL
	''')