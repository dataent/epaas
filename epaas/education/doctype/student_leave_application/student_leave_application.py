# -*- coding: utf-8 -*-
# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import dataent
from dataent import _
from dataent.utils import get_link_to_form
from dataent.model.document import Document

class StudentLeaveApplication(Document):
	def validate(self):
		self.validate_duplicate()

	def validate_duplicate(self):
		data = dataent.db.sql(""" select name from `tabStudent Leave Application`
			where
				((%(from_date)s > from_date and %(from_date)s < to_date) or
				(%(to_date)s > from_date and %(to_date)s < to_date) or
				(%(from_date)s <= from_date and %(to_date)s >= to_date)) and
				name != %(name)s and student = %(student)s and docstatus < 2
		""", {
			'from_date': self.from_date,
			'to_date': self.to_date,
			'student': self.student,
			'name': self.name
		}, as_dict=1)

		if data:
			link = get_link_to_form("Student Leave Application", data[0].name)
			dataent.throw(_("Leave application {0} already exists against the student {1}")
				.format(link, self.student))