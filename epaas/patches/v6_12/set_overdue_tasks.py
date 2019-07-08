from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doctype("Task")

	from epaas.projects.doctype.task.task import set_tasks_as_overdue
	set_tasks_as_overdue()
