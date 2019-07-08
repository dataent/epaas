from __future__ import unicode_literals

import dataent

def get_context(context):
	if dataent.form_dict.project:
		context.parents = [{'title': dataent.form_dict.project, 'route': '/projects?project='+ dataent.form_dict.project}]
		context.success_url = "/projects?project=" + dataent.form_dict.project
		
	elif context.doc and context.doc.get('project'):
		context.parents = [{'title': context.doc.project, 'route': '/projects?project='+ context.doc.project}]
		context.success_url = "/projects?project=" + context.doc.project
