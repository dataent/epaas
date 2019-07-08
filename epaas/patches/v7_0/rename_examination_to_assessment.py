# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

from dataent.model.utils.rename_field import rename_field

def execute():
	if dataent.db.exists("DocType", "Examination"):
		dataent.rename_doc("DocType", "Examination", "Assessment")
		dataent.rename_doc("DocType", "Examination Result", "Assessment Result")

		# 'Schools' module changed to the 'Education'
		# dataent.reload_doc("schools", "doctype", "assessment")
		# dataent.reload_doc("schools", "doctype", "assessment_result")

		dataent.reload_doc("education", "doctype", "assessment")
		dataent.reload_doc("education", "doctype", "assessment_result")

		rename_field("Assessment", "exam_name", "assessment_name")
		rename_field("Assessment", "exam_code", "assessment_code")
	
		dataent.db.sql("delete from `tabPortal Menu Item` where route = '/examination'")