from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doctype("Currency Exchange")
	dataent.db.sql("""
		update `tabCurrency Exchange` 
		set `date` = '2010-01-01' 
		where date is null or date = '0000-00-00'
	""")