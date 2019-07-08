from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doc("education", "doctype", "student_attendance")
	dataent.db.sql('''
		update `tabStudent Attendance` set
			docstatus=0
		where
			docstatus=1''')