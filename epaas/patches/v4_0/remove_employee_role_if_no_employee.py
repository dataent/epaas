# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent
import dataent.permissions

def execute():
	for user in dataent.db.sql_list("select distinct parent from `tabHas Role` where role='Employee'"):
		# if employee record does not exists, remove employee role!
		if not dataent.db.get_value("Employee", {"user_id": user}):
			try:
				user = dataent.get_doc("User", user)
				for role in user.get("roles", {"role": "Employee"}):
					user.get("roles").remove(role)
				user.save()
			except dataent.DoesNotExistError:
				pass
