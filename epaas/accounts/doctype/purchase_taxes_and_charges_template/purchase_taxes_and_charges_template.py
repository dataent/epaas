# -*- coding: utf-8 -*-
# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent
from dataent.model.document import Document
from epaas.accounts.doctype.sales_taxes_and_charges_template.sales_taxes_and_charges_template \
	import valdiate_taxes_and_charges_template

class PurchaseTaxesandChargesTemplate(Document):
	def validate(self):
		valdiate_taxes_and_charges_template(self)

	def autoname(self):
		if self.company and self.title:
			abbr = dataent.get_cached_value('Company',  self.company,  'abbr')
			self.name = '{0} - {1}'.format(self.title, abbr)
