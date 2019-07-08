# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

def execute():
	if not dataent.db.exists({"doctype": "Assessment Group","assessment_group_name": "All Assessment Groups"}):
		dataent.reload_doc("education", "doctype", "assessment_group")
		doc = dataent.new_doc("Assessment Group")
		doc.assessment_group_name = "All Assessment Groups"
		doc.is_group = 1
		doc.flags.ignore_mandatory = True
		doc.save()