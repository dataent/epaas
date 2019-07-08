# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent
import dataent.permissions

def execute():
	for warehouse, user in dataent.db.sql("""select parent, user from `tabWarehouse User`"""):
		dataent.permissions.add_user_permission("Warehouse", warehouse, user)

	dataent.delete_doc_if_exists("DocType", "Warehouse User")
	dataent.reload_doc("stock", "doctype", "warehouse")
