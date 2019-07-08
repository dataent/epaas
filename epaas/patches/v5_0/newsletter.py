# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent
import dataent.permissions

def execute():
	dataent.reload_doc("core", "doctype", "block_module")
	dataent.reload_doctype("User")
	dataent.reload_doctype("Lead")
	dataent.reload_doctype("Contact")

	dataent.reload_doc('email', 'doctype', 'email_group')
	dataent.reload_doc('email', 'doctype', 'email_group_member')
	dataent.reload_doc('email', 'doctype', 'newsletter')

	dataent.permissions.reset_perms("Newsletter")

	if not dataent.db.exists("Role", "Newsletter Manager"):
		dataent.get_doc({"doctype": "Role", "role": "Newsletter Manager"}).insert()

	for userrole in dataent.get_all("Has Role", "parent", {"role": "Sales Manager", "parenttype": "User"}):
		if dataent.db.exists("User", userrole.parent):
			user = dataent.get_doc("User", userrole.parent)
			user.append("roles", {
				"doctype": "Has Role",
				"role": "Newsletter Manager"
			})
			user.flags.ignore_mandatory = True
			user.save()

	# create default lists
	general = dataent.new_doc("Email Group")
	general.title = "General"
	general.insert()
	general.import_from("Lead")
	general.import_from("Contact")
