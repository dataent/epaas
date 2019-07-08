from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doc("stock", "doctype", "purchase_receipt")
	dataent.db.sql('''
		UPDATE `tabPurchase Receipt` SET status = "Completed" WHERE per_billed = 100 AND docstatus = 1
	''')