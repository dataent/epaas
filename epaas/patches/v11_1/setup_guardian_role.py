from __future__ import unicode_literals
import dataent

def execute():
	if 'Education' in dataent.get_active_domains() and not dataent.db.exists("Role", "Guardian"):
		doc = dataent.new_doc("Role")
		doc.update({
			"role_name": "Guardian",
			"desk_access": 0
		})

		doc.insert(ignore_permissions=True)
