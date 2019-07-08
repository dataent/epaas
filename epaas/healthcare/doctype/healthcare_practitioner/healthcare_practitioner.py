# -*- coding: utf-8 -*-
# Copyright (c) 2015, ESS LLP and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import dataent
from dataent.model.document import Document
from dataent import throw, _
from dataent.utils import cstr
from epaas.accounts.party import validate_party_accounts
from dataent.contacts.address_and_contact import load_address_and_contact, delete_contact_and_address
from dataent.desk.reportview import build_match_conditions, get_filters_cond

class HealthcarePractitioner(Document):
	def onload(self):
		load_address_and_contact(self)

	def autoname(self):
		# practitioner first_name and last_name
		self.name = " ".join(filter(None,
			[cstr(self.get(f)).strip() for f in ["first_name","middle_name","last_name"]]))

	def validate(self):
		validate_party_accounts(self)
		if self.inpatient_visit_charge_item:
			validate_service_item(self.inpatient_visit_charge_item, "Configure a service Item for Inpatient Visit Charge Item")
		if self.op_consulting_charge_item:
			validate_service_item(self.op_consulting_charge_item, "Configure a service Item for Out Patient Consulting Charge Item")

		if self.user_id:
			self.validate_for_enabled_user_id()
			self.validate_duplicate_user_id()
			existing_user_id = dataent.db.get_value("Healthcare Practitioner", self.name, "user_id")
			if self.user_id != existing_user_id:
				dataent.permissions.remove_user_permission(
					"Healthcare Practitioner", self.name, existing_user_id)

		else:
			existing_user_id = dataent.db.get_value("Healthcare Practitioner", self.name, "user_id")
			if existing_user_id:
				dataent.permissions.remove_user_permission(
					"Healthcare Practitioner", self.name, existing_user_id)

	def on_update(self):
		if self.user_id:
			dataent.permissions.add_user_permission("Healthcare Practitioner", self.name, self.user_id)


	def validate_for_enabled_user_id(self):
		enabled = dataent.db.get_value("User", self.user_id, "enabled")
		if enabled is None:
			dataent.throw(_("User {0} does not exist").format(self.user_id))
		if enabled == 0:
			dataent.throw(_("User {0} is disabled").format(self.user_id))

	def validate_duplicate_user_id(self):
		practitioner = dataent.db.sql_list("""select name from `tabHealthcare Practitioner` where
			user_id=%s and name!=%s""", (self.user_id, self.name))
		if practitioner:
			throw(_("User {0} is already assigned to Healthcare Practitioner {1}").format(
				self.user_id, practitioner[0]), dataent.DuplicateEntryError)

	def on_trash(self):
		delete_contact_and_address('Healthcare Practitioner', self.name)

def validate_service_item(item, msg):
	if dataent.db.get_value("Item", item, "is_stock_item") == 1:
		dataent.throw(_(msg))

def get_practitioner_list(doctype, txt, searchfield, start, page_len, filters=None):
	fields = ["name", "first_name", "mobile_phone"]
	match_conditions = build_match_conditions("Healthcare Practitioner")
	match_conditions = "and {}".format(match_conditions) if match_conditions else ""

	if filters:
		filter_conditions = get_filters_cond(doctype, filters, [])
		match_conditions += "{}".format(filter_conditions)

	return dataent.db.sql("""select %s from `tabHealthcare Practitioner` where docstatus < 2
		and (%s like %s or first_name like %s)
		and active = 1
		{match_conditions}
		order by
		case when name like %s then 0 else 1 end,
		case when first_name like %s then 0 else 1 end,
		name, first_name limit %s, %s""".format(
			match_conditions=match_conditions) %
			(
				", ".join(fields),
				dataent.db.escape(searchfield),
				"%s", "%s", "%s", "%s", "%s", "%s"
			),
			(
				"%%%s%%" % dataent.db.escape(txt),
				"%%%s%%" % dataent.db.escape(txt),
				"%%%s%%" % dataent.db.escape(txt),
				"%%%s%%" % dataent.db.escape(txt),
				start,
				page_len
			)
		)
