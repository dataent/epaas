# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent
from dataent import _
from dataent.utils import flt
from dataent.model.document import Document
from epaas.controllers.accounts_controller import validate_taxes_and_charges, validate_inclusive_tax

class SalesTaxesandChargesTemplate(Document):
	def validate(self):
		valdiate_taxes_and_charges_template(self)

	def autoname(self):
		if self.company and self.title:
			abbr = dataent.get_cached_value('Company',  self.company,  'abbr')
			self.name = '{0} - {1}'.format(self.title, abbr)

	def set_missing_values(self):
		for data in self.taxes:
			if data.charge_type == 'On Net Total' and flt(data.rate) == 0.0:
				data.rate = dataent.db.get_value('Account', data.account_head, 'tax_rate')

def valdiate_taxes_and_charges_template(doc):
	# default should not be disabled
	# if not doc.is_default and not dataent.get_all(doc.doctype, filters={"is_default": 1}):
	# 	doc.is_default = 1

	if doc.is_default == 1:
		dataent.db.sql("""update `tab{0}` set is_default = 0
			where is_default = 1 and name != %s and company = %s""".format(doc.doctype),
			(doc.name, doc.company))

	validate_disabled(doc)

	for tax in doc.get("taxes"):
		validate_taxes_and_charges(tax)
		validate_inclusive_tax(tax, doc)

def validate_disabled(doc):
	if doc.is_default and doc.disabled:
		dataent.throw(_("Disabled template must not be default template"))
