# Copyright (c) 2017, Dataent and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

def execute():
	""" delete deprecated reports """

	reports = [
		"Monthly Salary Register", "Customer Addresses And Contacts",
		"Supplier Addresses And Contacts"
	]

	for report in reports:
		if dataent.db.exists("Report", report):
			check_and_update_desktop_icon_for_report(report)
			check_and_update_auto_email_report(report)
			dataent.db.commit()

			dataent.delete_doc("Report", report, ignore_permissions=True)

def check_and_update_desktop_icon_for_report(report):
	""" delete or update desktop icon"""
	desktop_icons = dataent.db.sql_list("""select name from `tabDesktop Icon`
		where _report='{0}'""".format(report))

	if not desktop_icons:
		return

	if report == "Monthly Salary Register":
		for icon in desktop_icons:
			dataent.delete_doc("Desktop Icon", icon)

	elif report in ["Customer Addresses And Contacts", "Supplier Addresses And Contacts"]:
		dataent.db.sql("""update `tabDesktop Icon` set _report='{value}'
			where name in ({docnames})""".format(
				value="Addresses And Contacts",
				docnames=",".join(["'%s'"%icon for icon in desktop_icons])
			)
		)

def check_and_update_auto_email_report(report):
	""" delete or update auto email report for deprecated report """

	auto_email_report = dataent.db.get_value("Auto Email Report", {"report": report})
	if not auto_email_report:
		return

	if report == "Monthly Salary Register":
		dataent.delete_doc("Auto Email Report", auto_email_report)

	elif report in ["Customer Addresses And Contacts", "Supplier Addresses And Contacts"]:
		dataent.db.set_value("Auto Email Report", auto_email_report, "report", report)