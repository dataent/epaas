# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent
import dataent.defaults
from dataent import msgprint, _
from dataent.model.naming import set_name_by_naming_series
from dataent.contacts.address_and_contact import load_address_and_contact, delete_contact_and_address
from epaas.utilities.transaction_base import TransactionBase
from epaas.accounts.party import validate_party_accounts, get_dashboard_info, get_timeline_data # keep this


class Supplier(TransactionBase):
	def get_feed(self):
		return self.supplier_name

	def onload(self):
		"""Load address and contacts in `__onload`"""
		load_address_and_contact(self)
		self.load_dashboard_info()

	def before_save(self):
		if not self.on_hold:
			self.hold_type = ''
			self.release_date = ''
		elif self.on_hold and not self.hold_type:
			self.hold_type = 'All'

	def load_dashboard_info(self):
		info = get_dashboard_info(self.doctype, self.name)
		self.set_onload('dashboard_info', info)

	def autoname(self):
		supp_master_name = dataent.defaults.get_global_default('supp_master_name')
		if supp_master_name == 'Supplier Name':
			self.name = self.supplier_name
		else:
			set_name_by_naming_series(self)

	def on_update(self):
		if not self.naming_series:
			self.naming_series = ''

	def validate(self):
		# validation for Naming Series mandatory field...
		if dataent.defaults.get_global_default('supp_master_name') == 'Naming Series':
			if not self.naming_series:
				msgprint(_("Series is mandatory"), raise_exception=1)

		validate_party_accounts(self)

	def on_trash(self):
		delete_contact_and_address('Supplier', self.name)

	def after_rename(self, olddn, newdn, merge=False):
		if dataent.defaults.get_global_default('supp_master_name') == 'Supplier Name':
			dataent.db.set(self, "supplier_name", newdn)
