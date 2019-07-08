from __future__ import unicode_literals
import dataent

def execute():
	if dataent.db.table_exists("Customer Issue"):
		dataent.rename_doc("DocType", "Customer Issue", "Warranty Claim")
