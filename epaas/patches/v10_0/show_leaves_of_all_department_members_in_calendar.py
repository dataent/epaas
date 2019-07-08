from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doc("hr", "doctype", "hr_settings")
	dataent.db.set_value("HR Settings", None, "show_leaves_of_all_department_members_in_calendar", 1)