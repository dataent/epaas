from __future__ import unicode_literals
import dataent

def execute():
	if dataent.db.exists("DocType", "Guardian"):

		# 'Schools' module changed to the 'Education'
		# dataent.reload_doc("schools", "doctype", "student")
		# dataent.reload_doc("schools", "doctype", "student_guardian")
		# dataent.reload_doc("schools", "doctype", "student_sibling")

		dataent.reload_doc("education", "doctype", "student")
		dataent.reload_doc("education", "doctype", "student_guardian")
		dataent.reload_doc("education", "doctype", "student_sibling")
		if "student" not in dataent.db.get_table_columns("Guardian"):
			return
		guardian = dataent.get_all("Guardian", fields=["name", "student"])
		for d in guardian:
			if d.student:
				student = dataent.get_doc("Student", d.student)
				if student:
					student.append("guardians", {"guardian": d.name})
					student.save()
