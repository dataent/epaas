# Copyright (c) 2013, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doctype("Appraisal")
	dataent.db.sql("update `tabAppraisal` set remarks = comments")