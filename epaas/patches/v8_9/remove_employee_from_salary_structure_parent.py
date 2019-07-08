from __future__ import unicode_literals
import dataent

def execute():
	if 'employee' in dataent.db.get_table_columns("Salary Structure"):
		dataent.db.sql("alter table `tabSalary Structure` drop column employee")
