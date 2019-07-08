# Copyright (c) 2017, Dataent and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doc("projects", "doctype", "project_type")
	dataent.reload_doc("projects", "doctype", "project")

	project_types = ["Internal", "External", "Other"]

	for project_type in project_types:
		if not dataent.db.exists("Project Type", project_type):
			p_type = dataent.get_doc({
				"doctype": "Project Type",
				"project_type": project_type
			})
			p_type.insert()