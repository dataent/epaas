from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doc("accounts", "doctype", "account")
	
	dataent.db.sql(""" update tabAccount set account_type = "Stock"
		where account_type = "Warehouse" """)
	
	dataent.db.commit()