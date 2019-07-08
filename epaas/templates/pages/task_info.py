from __future__ import unicode_literals
import dataent

from dataent import _

def get_context(context):
	context.no_cache = 1

	task = dataent.get_doc('Task', dataent.form_dict.task)
	
	context.comments = dataent.get_all('Communication', filters={'reference_name': task.name, 'comment_type': 'comment'},
	fields=['subject', 'sender_full_name', 'communication_date'])
	
	context.doc = task