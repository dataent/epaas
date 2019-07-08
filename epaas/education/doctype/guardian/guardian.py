# -*- coding: utf-8 -*-
# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import dataent
from dataent import _
from dataent.model.document import Document
from dataent.utils.csvutils import getlink

class Guardian(Document):
	def __setup__(self):
		self.onload()

	def onload(self):
		"""Load Students for quick view"""
		self.load_students()

	def load_students(self):
		"""Load `students` from the database"""
		self.students = []
		students = dataent.get_all("Student Guardian", filters={"guardian":self.name}, fields=["parent"])
		for student in students:
			self.append("students", {
				"student":student.parent,
				"student_name": dataent.db.get_value("Student", student.parent, "title")
			})

	def validate(self):
		self.students = []


@dataent.whitelist()
def invite_guardian(guardian):
	guardian_doc = dataent.get_doc("Guardian", guardian)
	if not guardian_doc.email_address:
		dataent.throw(_("Please set Email Address"))
	else:
		guardian_as_user = dataent.get_value('User', dict(email=guardian_doc.email_address))
		if guardian_as_user:
			dataent.msgprint(_("User {0} already exists").format(getlink("User", guardian_as_user)))
			return guardian_as_user
		else:
			user = dataent.get_doc({
				"doctype": "User",
				"first_name": guardian_doc.guardian_name,
				"email": guardian_doc.email_address,
				"user_type": "Website User",
				"send_welcome_email": 1
			}).insert(ignore_permissions = True)
			dataent.msgprint(_("User {0} created").format(getlink("User", user.name)))
			return user.name
