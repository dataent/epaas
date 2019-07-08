from __future__ import unicode_literals
import dataent

def execute():
	dataent.db.sql("""UPDATE `tabDynamic Link` SET link_doctype = 'Lead' WHERE link_doctype = 'Load'""")
