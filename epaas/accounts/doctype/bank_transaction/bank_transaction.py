# -*- coding: utf-8 -*-
# Copyright (c) 2019, Dataent Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import dataent
from epaas.controllers.status_updater import StatusUpdater
from dataent.utils import flt
from six.moves import reduce
from dataent import _

class BankTransaction(StatusUpdater):
	def after_insert(self):
		self.unallocated_amount = abs(flt(self.credit) - flt(self.debit))

	def on_submit(self):
		self.clear_linked_payment_entries()
		self.set_status()

	def on_update_after_submit(self):
		self.update_allocations()
		self.clear_linked_payment_entries()
		self.set_status(update=True)

	def update_allocations(self):
		if self.payment_entries:
			allocated_amount = reduce(lambda x, y: flt(x) + flt(y), [x.allocated_amount for x in self.payment_entries])
		else:
			allocated_amount = 0

		if allocated_amount:
			dataent.db.set_value(self.doctype, self.name, "allocated_amount", flt(allocated_amount))
			dataent.db.set_value(self.doctype, self.name, "unallocated_amount", abs(flt(self.credit) - flt(self.debit)) - flt(allocated_amount))

		else:
			dataent.db.set_value(self.doctype, self.name, "allocated_amount", 0)
			dataent.db.set_value(self.doctype, self.name, "unallocated_amount", abs(flt(self.credit) - flt(self.debit)))

		amount = self.debit or self.credit
		if amount == self.allocated_amount:
			dataent.db.set_value(self.doctype, self.name, "status", "Reconciled")

		self.reload()

	def clear_linked_payment_entries(self):
		for payment_entry in self.payment_entries:
			allocated_amount = get_total_allocated_amount(payment_entry)
			paid_amount = get_paid_amount(payment_entry)

			if paid_amount and allocated_amount:
				if  flt(allocated_amount[0]["allocated_amount"]) > flt(paid_amount):
					dataent.throw(_("The total allocated amount ({0}) is greated than the paid amount ({1}).".format(flt(allocated_amount[0]["allocated_amount"]), flt(paid_amount))))
				elif flt(allocated_amount[0]["allocated_amount"]) == flt(paid_amount):
					if payment_entry.payment_document in ["Payment Entry", "Journal Entry", "Purchase Invoice", "Expense Claim"]:
						self.clear_simple_entry(payment_entry)

					elif payment_entry.payment_document == "Sales Invoice":
						self.clear_sales_invoice(payment_entry)

	def clear_simple_entry(self, payment_entry):
		dataent.db.set_value(payment_entry.payment_document, payment_entry.payment_entry, "clearance_date", self.date)

	def clear_sales_invoice(self, payment_entry):
		dataent.db.set_value("Sales Invoice Payment", dict(parenttype=payment_entry.payment_document,
			parent=payment_entry.payment_entry), "clearance_date", self.date)

def get_total_allocated_amount(payment_entry):
	return dataent.db.sql("""
		SELECT
			SUM(btp.allocated_amount) as allocated_amount,
			bt.name
		FROM
			`tabBank Transaction Payments` as btp
		LEFT JOIN
			`tabBank Transaction` bt ON bt.name=btp.parent
		WHERE
			btp.payment_document = %s
		AND
			btp.payment_entry = %s
		AND
			bt.docstatus = 1""", (payment_entry.payment_document, payment_entry.payment_entry), as_dict=True)

def get_paid_amount(payment_entry):
	if payment_entry.payment_document in ["Payment Entry", "Sales Invoice", "Purchase Invoice"]:
		return dataent.db.get_value(payment_entry.payment_document, payment_entry.payment_entry, "paid_amount")

	elif payment_entry.payment_document == "Journal Entry":
		return dataent.db.get_value(payment_entry.payment_document, payment_entry.payment_entry, "total_credit")

	elif payment_entry.payment_document == "Expense Claim":
		return dataent.db.get_value(payment_entry.payment_document, payment_entry.payment_entry, "total_amount_reimbursed")

	else:
		dataent.throw(_("Please reconcile {0}: {1} manually".format(payment_entry.payment_document, payment_entry.payment_entry)))

@dataent.whitelist()
def unclear_reference_payment(doctype, docname):
	if dataent.db.exists(doctype, docname):
		doc = dataent.get_doc(doctype, docname)
		if doctype == "Sales Invoice":
			dataent.db.set_value("Sales Invoice Payment", dict(parenttype=doc.payment_document,
				parent=doc.payment_entry), "clearance_date", None)
		else:
			dataent.db.set_value(doc.payment_document, doc.payment_entry, "clearance_date", None)

		return doc.payment_entry
