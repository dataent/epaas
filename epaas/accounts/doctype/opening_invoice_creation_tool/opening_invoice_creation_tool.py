# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dataent Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import dataent
from dataent import _, scrub
from dataent.utils import flt, nowdate
from dataent.model.document import Document


class OpeningInvoiceCreationTool(Document):
	def onload(self):
		"""Load the Opening Invoice summary"""
		summary, max_count = self.get_opening_invoice_summary()
		self.set_onload('opening_invoices_summary', summary)
		self.set_onload('max_count', max_count)
		self.set_onload('temporary_opening_account', get_temporary_opening_account(self.company))

	def get_opening_invoice_summary(self):
		def prepare_invoice_summary(doctype, invoices):
			# add company wise sales / purchase invoice summary
			paid_amount = []
			outstanding_amount = []
			for invoice in invoices:
				company = invoice.pop("company")
				_summary = invoices_summary.get(company, {})
				_summary.update({
					"currency": company_wise_currency.get(company),
					doctype: invoice
				})
				invoices_summary.update({company: _summary})

				paid_amount.append(invoice.paid_amount)
				outstanding_amount.append(invoice.outstanding_amount)

			if paid_amount or outstanding_amount:
				max_count.update({
					doctype: {
						"max_paid": max(paid_amount) if paid_amount else 0.0,
						"max_due": max(outstanding_amount) if outstanding_amount else 0.0
					}
				})

		invoices_summary = {}
		max_count = {}
		fields = [
			"company", "count(name) as total_invoices", "sum(outstanding_amount) as outstanding_amount"
		]
		companies = dataent.get_all("Company", fields=["name as company", "default_currency as currency"])
		if not companies:
			return None, None

		company_wise_currency = {row.company: row.currency for row in companies}
		for doctype in ["Sales Invoice", "Purchase Invoice"]:
			invoices = dataent.get_all(doctype, filters=dict(is_opening="Yes", docstatus=1),
				fields=fields, group_by="company")
			prepare_invoice_summary(doctype, invoices)

		return invoices_summary, max_count

	def make_invoices(self):
		names = []
		mandatory_error_msg = _("Row {0}: {1} is required to create the Opening {2} Invoices")
		if not self.company:
			dataent.throw(_("Please select the Company"))

		for row in self.invoices:
			if not row.qty:
				row.qty = 1.0

			# always mandatory fields for the invoices
			if not row.temporary_opening_account:
				row.temporary_opening_account = get_temporary_opening_account(self.company)
			row.party_type = "Customer" if self.invoice_type == "Sales" else "Supplier"

			# Allow to create invoice even if no party present in customer or supplier.
			if not dataent.db.exists(row.party_type, row.party):
				if self.create_missing_party:
					self.add_party(row.party_type, row.party)
				else:
					dataent.throw(_("{0} {1} does not exist.").format(dataent.bold(row.party_type), dataent.bold(row.party)))

			if not row.item_name:
				row.item_name = _("Opening Invoice Item")
			if not row.posting_date:
				row.posting_date = nowdate()
			if not row.due_date:
				row.due_date = nowdate()

			for d in ("Party", "Outstanding Amount", "Temporary Opening Account"):
				if not row.get(scrub(d)):
					dataent.throw(mandatory_error_msg.format(row.idx, _(d), self.invoice_type))

			args = self.get_invoice_dict(row=row)
			if not args:
				continue

			doc = dataent.get_doc(args).insert()
			doc.submit()
			names.append(doc.name)

			if len(self.invoices) > 5:
				dataent.publish_realtime(
					"progress", dict(
						progress=[row.idx, len(self.invoices)],
						title=_('Creating {0}').format(doc.doctype)
					),
					user=dataent.session.user
				)

		return names

	def add_party(self, party_type, party):
		party_doc = dataent.new_doc(party_type)
		if party_type == "Customer":
			party_doc.customer_name = party
		else:
			supplier_group = dataent.db.get_single_value("Buying Settings", "supplier_group")
			if not supplier_group:
				dataent.throw(_("Please Set Supplier Group in Buying Settings."))

			party_doc.supplier_name = party
			party_doc.supplier_group = supplier_group

		party_doc.flags.ignore_mandatory = True
		party_doc.save(ignore_permissions=True)

	def get_invoice_dict(self, row=None):
		def get_item_dict():
			default_uom = dataent.db.get_single_value("Stock Settings", "stock_uom") or _("Nos")
			cost_center = dataent.get_cached_value('Company',  self.company,  "cost_center")
			if not cost_center:
				dataent.throw(
					_("Please set the Default Cost Center in {0} company.").format(dataent.bold(self.company))
				)
			rate = flt(row.outstanding_amount) / flt(row.qty)

			return dataent._dict({
				"uom": default_uom,
				"rate": rate or 0.0,
				"qty": row.qty,
				"conversion_factor": 1.0,
				"item_name": row.item_name or "Opening Invoice Item",
				"description": row.item_name or "Opening Invoice Item",
				income_expense_account_field: row.temporary_opening_account,
				"cost_center": cost_center
			})

		if not row:
			return None

		party_type = "Customer"
		income_expense_account_field = "income_account"
		if self.invoice_type == "Purchase":
			party_type = "Supplier"
			income_expense_account_field = "expense_account"

		item = get_item_dict()

		args = dataent._dict({
			"items": [item],
			"is_opening": "Yes",
			"set_posting_time": 1,
			"company": self.company,
			"due_date": row.due_date,
			"posting_date": row.posting_date,
			dataent.scrub(party_type): row.party,
			"doctype": "Sales Invoice" if self.invoice_type == "Sales" else "Purchase Invoice",
			"currency": dataent.get_cached_value('Company',  self.company,  "default_currency")
		})

		if self.invoice_type == "Sales":
			args["is_pos"] = 0

		return args

@dataent.whitelist()
def get_temporary_opening_account(company=None):
	if not company:
		return

	accounts = dataent.get_all("Account", filters={
		'company': company,
		'account_type': 'Temporary'
	})
	if not accounts:
		dataent.throw(_("Please add a Temporary Opening account in Chart of Accounts"))

	return accounts[0].name


