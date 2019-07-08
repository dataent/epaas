from __future__ import unicode_literals
import dataent

def execute():
	for project in dataent.db.sql_list("select name from tabProject"):
		dataent.reload_doc("projects", "doctype", "project")
		p = dataent.get_doc("Project", project)
		p.update_milestones_completed()
		p.db_set("percent_milestones_completed", p.percent_milestones_completed)
