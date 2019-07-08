from __future__ import unicode_literals
import dataent

def pre_process(issue):

	project = dataent.db.get_value('Project', filters={'project_name': issue.milestone})
	return {
		'title': issue.title,
		'body': dataent.utils.md_to_html(issue.body or ''),
		'state': issue.state.title(),
		'project': project or ''
	}
