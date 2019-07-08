from __future__ import unicode_literals
import dataent

def execute():
	ps = dataent.db.get_value('Property Setter', dict(doc_type='Project', field_name='project_type',
		property='options'))
	if ps:
		dataent.delete_doc('Property Setter', ps)

	project_types = dataent.db.sql_list('select distinct project_type from tabProject')

	for project_type in project_types:
		if project_type and not dataent.db.exists("Project Type", project_type):
			p_type = dataent.get_doc({
				"doctype": "Project Type",
				"project_type": project_type
			})
			p_type.insert()