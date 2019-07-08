# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dataent Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import dataent
from dataent.model.document import Document
from dataent.utils import flt, cint
from dataent import _


class PaymentTermsTemplate(Document):
	def validate(self):
		self.validate_invoice_portion()
		self.validate_credit_days()
		self.check_duplicate_terms()

	def validate_invoice_portion(self):
		total_portion = 0
		for term in self.terms:
			total_portion += flt(term.get('invoice_portion', 0))

		if flt(total_portion, 2) != 100.00:
			dataent.msgprint(_('Combined invoice portion must equal 100%'), raise_exception=1, indicator='red')

	def validate_credit_days(self):
		for term in self.terms:
			if cint(term.credit_days) < 0:
				dataent.msgprint(_('Credit Days cannot be a negative number'), raise_exception=1, indicator='red')

	def check_duplicate_terms(self):
		terms = []
		for term in self.terms:
			term_info = (term.credit_days, term.due_date_based_on)
			if term_info in terms:
				dataent.msgprint(
					_('The Payment Term at row {0} is possibly a duplicate.').format(term.idx),
					raise_exception=1, indicator='red'
				)
			else:
				terms.append(term_info)
