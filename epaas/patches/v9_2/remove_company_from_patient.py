from __future__ import unicode_literals
import dataent

def execute():
	if dataent.db.exists("DocType", "Patient"):
		if 'company' in dataent.db.get_table_columns("Patient"):
			dataent.db.sql("alter table `tabPatient` drop column company")
