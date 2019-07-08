from __future__ import unicode_literals
import dataent

def execute():
	if dataent.db.table_exists("Time Log"):
		dataent.db.sql("""delete from `tabDocType`
			where name in('Time Log Batch', 'Time Log Batch Detail', 'Time Log')""")

	dataent.db.sql("""delete from `tabDocField` where parent in ('Time Log', 'Time Log Batch')""")
	dataent.db.sql("""update `tabCustom Script` set dt = 'Timesheet' where dt = 'Time Log'""")

	for data in dataent.db.sql(""" select label, fieldname from  `tabCustom Field` where dt = 'Time Log'""", as_dict=1):
		custom_field = dataent.get_doc({
			'doctype': 'Custom Field',
			'label': data.label,
			'dt': 'Timesheet Detail',
			'fieldname': data.fieldname,
			'fieldtype': data.fieldtype or "Data"
		}).insert(ignore_permissions=True)

	dataent.db.sql("""delete from `tabCustom Field` where dt = 'Time Log'""")
	dataent.reload_doc('projects', 'doctype', 'timesheet')
	dataent.reload_doc('projects', 'doctype', 'timesheet_detail')

	report = "Daily Time Log Summary"
	if dataent.db.exists("Report", report):
		dataent.delete_doc('Report', report)
