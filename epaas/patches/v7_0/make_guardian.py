from __future__ import unicode_literals
import dataent

def execute():
	if dataent.db.exists("DocType", "Student"):
		student_table_cols = dataent.db.get_table_columns("Student")
		if "father_name" in student_table_cols:

			# 'Schools' module changed to the 'Education'
			# dataent.reload_doc("schools", "doctype", "student")
			# dataent.reload_doc("schools", "doctype", "guardian")
			# dataent.reload_doc("schools", "doctype", "guardian_interest")

			dataent.reload_doc("education", "doctype", "student")
			dataent.reload_doc("education", "doctype", "guardian")
			dataent.reload_doc("education", "doctype", "guardian_interest")
			dataent.reload_doc("hr", "doctype", "interest")
		
			fields = ["name", "father_name", "mother_name"]
			
			if "father_email_id" in student_table_cols:
				fields += ["father_email_id", "mother_email_id"]
	
			students = dataent.get_all("Student", fields)
			for stud in students:
				if stud.father_name:
					make_guardian(stud.father_name, stud.name, stud.father_email_id)
				if stud.mother_name:
					make_guardian(stud.mother_name, stud.name, stud.mother_email_id)
		
def make_guardian(name, student, email=None):
	dataent.get_doc({
		'doctype': 'Guardian',
		'guardian_name': name,
		'email': email,
		'student': student
	}).insert()
