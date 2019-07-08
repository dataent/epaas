# -*- coding: utf-8 -*-
# Copyright (c) 2015, Dataent Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import dataent
from dataent.model.document import Document
from dataent import _
from dataent.utils import cstr
from epaas.education.api import get_student_group_students


class StudentAttendance(Document):
	def validate(self):
		self.validate_date()
		self.validate_mandatory()
		self.validate_course_schedule()
		self.validate_student()
		self.validate_duplication()
		
	def validate_date(self):
		if self.course_schedule:
			self.date = dataent.db.get_value("Course Schedule", self.course_schedule, "schedule_date")
	
	def validate_mandatory(self):
		if not (self.student_group or self.course_schedule):
			dataent.throw(_("""Student Group or Course Schedule is mandatory"""))
	
	def validate_course_schedule(self):
		if self.course_schedule:
			self.student_group = dataent.db.get_value("Course Schedule", self.course_schedule, "student_group")
	
	def validate_student(self):
		if self.course_schedule:
			student_group = dataent.db.get_value("Course Schedule", self.course_schedule, "student_group")
		else:
			student_group = self.student_group
		student_group_students = [d.student for d in get_student_group_students(student_group)]
		if student_group and self.student not in student_group_students:
			dataent.throw(_('''Student {0}: {1} does not belong to Student Group {2}'''.format(self.student, self.student_name, student_group)))

	def validate_duplication(self):
		"""Check if the Attendance Record is Unique"""
		attendance_records=None
		if self.course_schedule:
			attendance_records= dataent.db.sql("""select name from `tabStudent Attendance` where \
				student= %s and ifnull(course_schedule, '')= %s and name != %s""",
				(self.student, cstr(self.course_schedule), self.name))
		else:
			attendance_records= dataent.db.sql("""select name from `tabStudent Attendance` where \
				student= %s and student_group= %s and date= %s and name != %s and \
				(course_schedule is Null or course_schedule='')""",
				(self.student, self.student_group, self.date, self.name))
			
		if attendance_records:
			dataent.throw(_("Attendance Record {0} exists against Student {1}")
				.format(attendance_records[0][0], self.student))
