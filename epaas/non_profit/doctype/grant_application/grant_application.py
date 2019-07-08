# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dataent Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import dataent
from dataent import _
from dataent.website.website_generator import WebsiteGenerator
from dataent.contacts.address_and_contact import load_address_and_contact
from dataent.utils import get_url

class GrantApplication(WebsiteGenerator):
	_website = dataent._dict(
		condition_field = "published",
	)

	def validate(self):
		if not self.route:	#pylint: disable=E0203
			self.route = 'grant-application/' + self.scrub(self.name)

	def onload(self):
		"""Load address and contacts in `__onload`"""
		load_address_and_contact(self)

	def get_context(self, context):
		context.no_cache = True
		context.show_sidebar = True
		context.parents = [dict(label='View All Grant Applications',
			route='grant-application', title='View Grants')]

def get_list_context(context):
	context.allow_guest = True
	context.no_cache = True
	context.no_breadcrumbs = True
	context.show_sidebar = True
	context.order_by = 'creation desc'
	context.introduction ='''<a class="btn btn-primary" href="/my-grant?new=1">
		Apply for new Grant Application</a>'''

@dataent.whitelist()
def send_grant_review_emails(grant_application):
	grant = dataent.get_doc("Grant Application", grant_application)
	url =  get_url('grant-application/{0}'.format(grant_application))
	dataent.sendmail(
		recipients= grant.assessment_manager,
		sender=dataent.session.user,
		subject='Grant Application for {0}'.format(grant.applicant_name),
		message='<p> Please Review this grant application</p><br>' + url,
		reference_doctype=grant.doctype,
		reference_name=grant.name
	)

	grant.status = 'In Progress'
	grant.email_notification_sent = 1
	grant.save()
	dataent.db.commit()

	dataent.msgprint(_("Review Invitation Sent"))