# -*- coding: utf-8 -*-
# Copyright (c) 2018, Dataent Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import dataent
from dataent import _
from dataent.utils import nowdate
from epaas.accounts.party import get_party_account
from dataent.model.document import Document

class PaymentOrder(Document):
	def on_submit(self):
		self.update_payment_request_status()

	def on_cancel(self):
		self.update_payment_request_status(cancel=True)

	def update_payment_request_status(self, cancel=False):
		status = 'Payment Ordered'
		if cancel:
			status = 'Initiated'

		for d in self.references:
			dataent.db.set_value('Payment Request', d.payment_request, 'status', status)

def get_mop_query(doctype, txt, searchfield, start, page_len, filters):
	return dataent.db.sql(""" select mode_of_payment from `tabPayment Order Reference`
		where parent = %(parent)s and mode_of_payment like %(txt)s
		limit %(start)s, %(page_len)s""", {
			'parent': filters.get("parent"),
			'start': start,
			'page_len': page_len,
			'txt': "%%%s%%" % txt
		})

def get_supplier_query(doctype, txt, searchfield, start, page_len, filters):
	return dataent.db.sql(""" select supplier from `tabPayment Order Reference`
		where parent = %(parent)s and supplier like %(txt)s and
		(payment_reference is null or payment_reference='')
		limit %(start)s, %(page_len)s""", {
			'parent': filters.get("parent"),
			'start': start,
			'page_len': page_len,
			'txt': "%%%s%%" % txt
		})

@dataent.whitelist()
def make_payment_records(name, supplier, mode_of_payment=None):
	doc = dataent.get_doc('Payment Order', name)
	make_journal_entry(doc, supplier, mode_of_payment)

def make_journal_entry(doc, supplier, mode_of_payment=None):
	je = dataent.new_doc('Journal Entry')
	je.payment_order = doc.name
	je.posting_date = nowdate()
	mode_of_payment_type = dataent._dict(dataent.get_all('Mode of Payment',
		fields = ["name", "type"], as_list=1))

	je.voucher_type = 'Bank Entry'
	if mode_of_payment and mode_of_payment_type.get(mode_of_payment) == 'Cash':
		je.voucher_type = "Cash Entry"
		
	paid_amt = 0
	party_account = get_party_account('Supplier', supplier, doc.company)
	for d in doc.references:
		if (d.supplier == supplier
			and (not mode_of_payment or mode_of_payment == d.mode_of_payment)):
			je.append('accounts', {
				'account': party_account,
				'debit_in_account_currency': d.amount,
				'party_type': 'Supplier',
				'party': supplier,
				'reference_type': d.reference_doctype,
				'reference_name': d.reference_name
			})

			paid_amt += d.amount

	je.append('accounts', {
		'account': doc.references[0].account,
		'credit_in_account_currency': paid_amt
	})

	je.flags.ignore_mandatory = True
	je.save()
	dataent.msgprint(_("{0} {1} created").format(je.doctype, je.name))
