from __future__ import unicode_literals
import dataent

def execute():
	if dataent.db.exists("DocType", "Leave Type"):
		if 'max_days_allowed' in dataent.db.get_table_columns("Leave Type"):
			dataent.db.sql("alter table `tabLeave Type` drop column max_days_allowed")