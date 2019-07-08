# Copyright (c) 2017, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

def execute():
	""" delete doctypes """

	if dataent.db.exists("DocType", "Grading Structure"):
		dataent.delete_doc("DocType", "Grading Structure", force=1)

	if dataent.db.exists("DocType", "Grade Interval"):
		dataent.delete_doc("DocType", "Grade Interval", force=1)