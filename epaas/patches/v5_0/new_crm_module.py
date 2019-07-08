# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import json
import dataent

def execute():
	dataent.reload_doc('crm', 'doctype', 'lead')
	dataent.reload_doc('crm', 'doctype', 'opportunity')

	add_crm_to_user_desktop_items()

def add_crm_to_user_desktop_items():
	key = "_user_desktop_items"
	for user in dataent.get_all("User", filters={"enabled": 1, "user_type": "System User"}):
		user = user.name
		user_desktop_items = dataent.db.get_defaults(key, parent=user)
		if user_desktop_items:
			user_desktop_items = json.loads(user_desktop_items)
			if "CRM" not in user_desktop_items:
				user_desktop_items.append("CRM")
				dataent.db.set_default(key, json.dumps(user_desktop_items), parent=user)

