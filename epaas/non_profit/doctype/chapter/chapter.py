# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dataent Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import dataent
from dataent.website.website_generator import WebsiteGenerator

class Chapter(WebsiteGenerator):
	_website = dataent._dict(
		condition_field = "published",
	)

	def get_context(self, context):
		context.no_cache = True
		context.show_sidebar = True
		context.parents = [dict(label='View All Chapters',
			route='chapters', title='View Chapters')]

	def validate(self):
		if not self.route:		#pylint: disable=E0203
			self.route = 'chapters/' + self.scrub(self.name)

	def enable(self):
		chapter = dataent.get_doc('Chapter', dataent.form_dict.name)
		chapter.append('members', dict(enable=self.value))
		chapter.save(ignore_permissions=1)
		dataent.db.commit()


def get_list_context(context):
	context.allow_guest = True
	context.no_cache = True
	context.show_sidebar = True
	context.title = 'All Chapters'
	context.no_breadcrumbs = True
	context.order_by = 'creation desc'


@dataent.whitelist()
def leave(title, user_id, leave_reason):
	chapter = dataent.get_doc("Chapter", title)
	for member in chapter.members:
		if member.user == user_id:
			member.enabled = 0
			member.leave_reason = leave_reason
	chapter.save(ignore_permissions=1)
	dataent.db.commit()
	return "Thank you for Feedback"
