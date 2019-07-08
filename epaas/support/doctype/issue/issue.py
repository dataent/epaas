# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent
import json
from dataent import _

from dataent.model.document import Document
from dataent.utils import now
from dataent.utils.user import is_website_user
from dataent.email.inbox import link_communication_to_document

sender_field = "raised_by"

class Issue(Document):
	def get_feed(self):
		return "{0}: {1}".format(_(self.status), self.subject)

	def validate(self):
		if (self.get("__islocal") and self.via_customer_portal):
			self.flags.create_communication = True
		if not self.raised_by:
			self.raised_by = dataent.session.user
		self.update_status()
		self.set_lead_contact(self.raised_by)

		if self.status == "Closed":
			from dataent.desk.form.assign_to import clear
			clear(self.doctype, self.name)

	def on_update(self):
		# create the communication email and remove the description
		if (self.flags.create_communication and self.via_customer_portal):
			self.create_communication()
			self.flags.communication_created = None

	def set_lead_contact(self, email_id):
		import email.utils
		email_id = email.utils.parseaddr(email_id)[1]
		if email_id:
			if not self.lead:
				self.lead = dataent.db.get_value("Lead", {"email_id": email_id})
			if not self.contact and not self.customer:
				self.contact = dataent.db.get_value("Contact", {"email_id": email_id})

				if self.contact:
					contact = dataent.get_doc('Contact', self.contact)
					self.customer = contact.get_link_for('Customer')

			if not self.company:
				self.company = dataent.db.get_value("Lead", self.lead, "company") or \
					dataent.db.get_default("Company")

	def update_status(self):
		status = dataent.db.get_value("Issue", self.name, "status")
		if self.status!="Open" and status =="Open" and not self.first_responded_on:
			self.first_responded_on = now()
		if self.status=="Closed" and status !="Closed":
			self.resolution_date = now()
		if self.status=="Open" and status !="Open":
			# if no date, it should be set as None and not a blank string "", as per mysql strict config
			self.resolution_date = None

	def create_communication(self):
		communication = dataent.new_doc("Communication")
		communication.update({
			"communication_type": "Communication",
			"communication_medium": "Email",
			"sent_or_received": "Received",
			"email_status": "Open",
			"subject": self.subject,
			"sender": self.raised_by,
			"content": self.description,
			"status": "Linked",
			"reference_doctype": "Issue",
			"reference_name": self.name
		})
		communication.ignore_permissions = True
		communication.ignore_mandatory = True
		communication.save()

		self.db_set("description", "")

	def split_issue(self, subject, communication_id):
		# Bug: Pressing enter doesn't send subject
		from copy import deepcopy
		replicated_issue = deepcopy(self)
		replicated_issue.subject = subject
		dataent.get_doc(replicated_issue).insert()
		# Replicate linked Communications
		# todo get all communications in timeline before this, and modify them to append them to new doc
		comm_to_split_from = dataent.get_doc("Communication", communication_id)
		communications = dataent.get_all("Communication", filters={"reference_name": comm_to_split_from.reference_name, "reference_doctype": "Issue", "creation": ('>=', comm_to_split_from.creation)})
		for communication in communications:
			doc = dataent.get_doc("Communication", communication.name)
			doc.reference_name = replicated_issue.name
			doc.save(ignore_permissions=True)
		return replicated_issue.name

def get_list_context(context=None):
	return {
		"title": _("Issues"),
		"get_list": get_issue_list,
		"row_template": "templates/includes/issue_row.html",
		"show_sidebar": True,
		"show_search": True,
		'no_breadcrumbs': True
	}

def get_issue_list(doctype, txt, filters, limit_start, limit_page_length=20, order_by=None):
	from dataent.www.list import get_list
	user = dataent.session.user
	contact = dataent.db.get_value('Contact', {'user': user}, 'name')
	customer = None
	if contact:
		contact_doc = dataent.get_doc('Contact', contact)
		customer = contact_doc.get_link_for('Customer')

	ignore_permissions = False
	if is_website_user():
		if not filters: filters = []
		filters.append(("Issue", "customer", "=", customer)) if customer else filters.append(("Issue", "raised_by", "=", user))
		ignore_permissions = True

	return get_list(doctype, txt, filters, limit_start, limit_page_length, ignore_permissions=ignore_permissions)

@dataent.whitelist()
def set_status(name, status):
	st = dataent.get_doc("Issue", name)
	st.status = status
	st.save()

def auto_close_tickets():
	""" auto close the replied support tickets after 7 days """
	auto_close_after_days = dataent.db.get_value("Support Settings", "Support Settings", "close_issue_after_days") or 7

	issues = dataent.db.sql(""" select name from tabIssue where status='Replied' and
		modified<DATE_SUB(CURDATE(), INTERVAL %s DAY) """, (auto_close_after_days), as_dict=True)

	for issue in issues:
		doc = dataent.get_doc("Issue", issue.get("name"))
		doc.status = "Closed"
		doc.flags.ignore_permissions = True
		doc.flags.ignore_mandatory = True
		doc.save()

@dataent.whitelist()
def set_multiple_status(names, status):
	names = json.loads(names)
	for name in names:
		set_status(name, status)

def has_website_permission(doc, ptype, user, verbose=False):
	from epaas.controllers.website_list_for_contact import has_website_permission
	permission_based_on_customer = has_website_permission(doc, ptype, user, verbose)

	return permission_based_on_customer or doc.raised_by==user


def update_issue(contact, method):
	"""Called when Contact is deleted"""
	dataent.db.sql("""UPDATE `tabIssue` set contact='' where contact=%s""", contact.name)

@dataent.whitelist()
def make_issue_from_communication(communication, ignore_communication_links=False):
	""" raise a issue from email """

	doc = dataent.get_doc("Communication", communication)
	issue = dataent.get_doc({
		"doctype": "Issue",
		"subject": doc.subject,
		"communication_medium": doc.communication_medium,
		"raised_by": doc.sender or "",
		"raised_by_phone": doc.phone_no or ""
	}).insert(ignore_permissions=True)

	link_communication_to_document(doc, "Issue", issue.name, ignore_communication_links)

	return issue.name