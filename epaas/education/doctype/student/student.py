# -*- coding: utf-8 -*-
# Copyright (c) 2015, Dataent Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import dataent
from dataent.model.document import Document
from dataent import _
from dataent.desk.form.linked_with import get_linked_doctypes

class Student(Document):
	def validate(self):
		self.title = " ".join(filter(None, [self.first_name, self.middle_name, self.last_name]))

		if self.student_applicant:
			self.check_unique()
			self.update_applicant_status()

		if dataent.get_value("Student", self.name, "title") != self.title:
			self.update_student_name_in_linked_doctype()

	def update_student_name_in_linked_doctype(self):
		linked_doctypes = get_linked_doctypes("Student")
		for d in linked_doctypes:
			meta = dataent.get_meta(d)
			if not meta.issingle:
				if "student_name" in [f.fieldname for f in meta.fields]:
					dataent.db.sql("""UPDATE `tab{0}` set student_name = %s where {1} = %s"""
						.format(d, linked_doctypes[d]["fieldname"][0]),(self.title, self.name))

				if "child_doctype" in linked_doctypes[d].keys() and "student_name" in \
					[f.fieldname for f in dataent.get_meta(linked_doctypes[d]["child_doctype"]).fields]:
					dataent.db.sql("""UPDATE `tab{0}` set student_name = %s where {1} = %s"""
						.format(linked_doctypes[d]["child_doctype"], linked_doctypes[d]["fieldname"][0]),(self.title, self.name))

	def check_unique(self):
		"""Validates if the Student Applicant is Unique"""
		student = dataent.db.sql("select name from `tabStudent` where student_applicant=%s and name!=%s", (self.student_applicant, self.name))
		if student:
			dataent.throw(_("Student {0} exist against student applicant {1}").format(student[0][0], self.student_applicant))

	def update_applicant_status(self):
		"""Updates Student Applicant status to Admitted"""
		if self.student_applicant:
			dataent.db.set_value("Student Applicant", self.student_applicant, "application_status", "Admitted")

def get_timeline_data(doctype, name):
	'''Return timeline for attendance'''
	return dict(dataent.db.sql('''select unix_timestamp(`date`), count(*)
		from `tabStudent Attendance` where
			student=%s
			and `date` > date_sub(curdate(), interval 1 year)
			and status = 'Present'
			group by date''', name))
