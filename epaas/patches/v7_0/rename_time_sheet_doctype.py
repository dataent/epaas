from __future__ import unicode_literals
import dataent

def execute():
	if dataent.db.table_exists("Time Sheet") and not dataent.db.table_exists("Timesheet"):
		dataent.rename_doc("DocType", "Time Sheet", "Timesheet")
		dataent.rename_doc("DocType", "Time Sheet Detail", "Timesheet Detail")
		
		for doctype in ['Time Sheet', 'Time Sheet Detail']:
			dataent.delete_doc('DocType', doctype)
		
		report = "Daily Time Sheet Summary"
		if dataent.db.exists("Report", report):
			dataent.delete_doc('Report', report)
