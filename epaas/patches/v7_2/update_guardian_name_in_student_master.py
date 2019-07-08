from __future__ import unicode_literals
import dataent
from dataent.model.utils.rename_field import rename_field

def execute():
	# 'Schools' module changed to the 'Education'
	# dataent.reload_doc("schools", "doctype", "student_guardian")
	dataent.reload_doc("education", "doctype", "student_guardian")

	student_guardians = dataent.get_all("Student Guardian", fields=["guardian"])
	for student_guardian in student_guardians:
		guardian_name = dataent.db.get_value("Guardian", student_guardian.guardian, "guardian_name")
		dataent.db.sql("update `tabStudent Guardian` set guardian_name = %s where guardian= %s",
			(guardian_name, student_guardian.guardian))