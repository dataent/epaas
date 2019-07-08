from __future__ import unicode_literals
import dataent

def execute():
	dataent.db.sql("""
		update `tabSalary Structure` ss, `tabSalary Detail` sd
		set sd.docstatus=1
		where ss.name=sd.parent and ss.docstatus=1 and sd.parenttype='Salary Structure'
	""")
