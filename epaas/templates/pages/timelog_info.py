from __future__ import unicode_literals
import dataent

from dataent import _

def get_context(context):
	context.no_cache = 1

	timelog = dataent.get_doc('Time Log', dataent.form_dict.timelog)
	
	context.doc = timelog