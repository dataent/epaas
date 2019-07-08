from __future__ import unicode_literals
import dataent

def get_context(context):
	context.no_cache = True
	chapter = dataent.get_doc('Chapter', dataent.form_dict.name)
	context.member_deleted = True
	context.chapter = chapter
