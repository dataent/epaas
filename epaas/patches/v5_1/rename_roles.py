from __future__ import unicode_literals
import dataent

def execute():
	if not dataent.db.exists("Role", "Stock User"):
		dataent.rename_doc("Role", "Material User", "Stock User")
	if not dataent.db.exists("Role", "Stock Manager"):
		dataent.rename_doc("Role", "Material Manager", "Stock Manager")
	if not dataent.db.exists("Role", "Item Manager"):
		dataent.rename_doc("Role", "Material Master Manager", "Item Manager")
