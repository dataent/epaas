from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doc('setup','doctype','sales_person')
	dataent.db.sql("""update `tabSales Person` set enabled=1 
		where (employee is null or employee = '' 
			or employee IN (select employee from tabEmployee where status != "Left"))""")
