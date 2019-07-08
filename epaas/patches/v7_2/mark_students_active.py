from __future__ import unicode_literals
import dataent

def execute():
	# 'Schools' module changed to the 'Education'
	# dataent.reload_doc('schools', 'doctype', 'student_group_student')

	dataent.reload_doc('education', 'doctype', 'student_group_student')
	dataent.db.sql("update `tabStudent Group Student` set active=1")
