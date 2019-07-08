# Copyright (c) 2018, Dataent and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent


def execute():
	if not dataent.db.table_exists('Daily Work Summary Group'):
		dataent.reload_doc("hr", "doctype", "daily_work_summary_group")
		dataent.reload_doc("hr", "doctype", "daily_work_summary_group_user")

		# check if Daily Work Summary Settings Company table exists
		try:
			dataent.db.sql('DESC `tabDaily Work Summary Settings Company`')
		except Exception:
			return

		# get the previously saved settings
		previous_setting = get_previous_setting()
		if previous_setting["companies"]:
			for d in previous_setting["companies"]:
				users = dataent.get_list("Employee", dict(
					company=d.company, user_id=("!=", " ")), "user_id as user")
				if(len(users)):
					# create new group entry for each company entry
					new_group = dataent.get_doc(dict(doctype="Daily Work Summary Group",
						name="Daily Work Summary for " + d.company,
						users=users,
						send_emails_at=d.send_emails_at,
						subject=previous_setting["subject"],
						message=previous_setting["message"]))
					new_group.flags.ignore_permissions = True
					new_group.flags.ignore_validate = True
					new_group.insert(ignore_if_duplicate = True)

	dataent.delete_doc("DocType", "Daily Work Summary Settings")
	dataent.delete_doc("DocType", "Daily Work Summary Settings Company")


def get_previous_setting():
	obj = {}
	setting_data = dataent.db.sql(
		"select field, value from tabSingles where doctype='Daily Work Summary Settings'")
	for field, value in setting_data:
		obj[field] = value
	obj["companies"] = get_setting_companies()
	return obj

def get_setting_companies():
	return dataent.db.sql("select * from `tabDaily Work Summary Settings Company`", as_dict=True)