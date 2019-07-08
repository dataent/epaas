
# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals

import dataent
import random
from dataent.utils import random_string
from dataent.desk import query_report
from epaas.accounts.doctype.journal_entry.journal_entry import get_payment_entry_against_invoice
from epaas.accounts.doctype.payment_entry.payment_entry import get_payment_entry
from dataent.utils.make_random import get_random
from epaas.accounts.doctype.payment_request.payment_request import make_payment_request, make_payment_entry
from epaas.demo.user.sales import make_sales_order
from epaas.selling.doctype.sales_order.sales_order import make_sales_invoice
from epaas.stock.doctype.purchase_receipt.purchase_receipt import make_purchase_invoice

def work():
	dataent.set_user(dataent.db.get_global('demo_accounts_user'))

	if random.random() <= 0.6:
		report = "Ordered Items to be Billed"
		for so in list(set([r[0] for r in query_report.run(report)["result"]
				if r[0]!="Total"]))[:random.randint(1, 5)]:
			try:
				si = dataent.get_doc(make_sales_invoice(so))
				si.posting_date = dataent.flags.current_date
				for d in si.get("items"):
					if not d.income_account:
						d.income_account = "Sales - {}".format(dataent.get_cached_value('Company',  si.company,  'abbr'))
				si.insert()
				si.submit()
				dataent.db.commit()
			except dataent.ValidationError:
				pass

	if random.random() <= 0.6:
		report = "Received Items to be Billed"
		for pr in list(set([r[0] for r in query_report.run(report)["result"]
			if r[0]!="Total"]))[:random.randint(1, 5)]:
			try:
				pi = dataent.get_doc(make_purchase_invoice(pr))
				pi.posting_date = dataent.flags.current_date
				pi.bill_no = random_string(6)
				pi.insert()
				pi.submit()
				dataent.db.commit()
			except dataent.ValidationError:
				pass


	if random.random() < 0.5:
		make_payment_entries("Sales Invoice", "Accounts Receivable")

	if random.random() < 0.5:
		make_payment_entries("Purchase Invoice", "Accounts Payable")

	if random.random() < 0.4:
		#make payment request against sales invoice
		sales_invoice_name = get_random("Sales Invoice", filters={"docstatus": 1})
		if sales_invoice_name:
			si = dataent.get_doc("Sales Invoice", sales_invoice_name)
			if si.outstanding_amount > 0:
				payment_request = make_payment_request(dt="Sales Invoice", dn=si.name, recipient_id=si.contact_email,
					submit_doc=True, mute_email=True, use_dummy_message=True)

				payment_entry = dataent.get_doc(make_payment_entry(payment_request.name))
				payment_entry.posting_date = dataent.flags.current_date
				payment_entry.submit()

	make_pos_invoice()

def make_payment_entries(ref_doctype, report):
	outstanding_invoices = list(set([r[3] for r in query_report.run(report,
	{"report_date": dataent.flags.current_date })["result"] if r[2]==ref_doctype]))

	# make Payment Entry
	for inv in outstanding_invoices[:random.randint(1, 2)]:
		pe = get_payment_entry(ref_doctype, inv)
		pe.posting_date = dataent.flags.current_date
		pe.reference_no = random_string(6)
		pe.reference_date = dataent.flags.current_date
		pe.insert()
		pe.submit()
		dataent.db.commit()
		outstanding_invoices.remove(inv)

	# make payment via JV
	for inv in outstanding_invoices[:1]:
		jv = dataent.get_doc(get_payment_entry_against_invoice(ref_doctype, inv))
		jv.posting_date = dataent.flags.current_date
		jv.cheque_no = random_string(6)
		jv.cheque_date = dataent.flags.current_date
		jv.insert()
		jv.submit()
		dataent.db.commit()

def make_pos_invoice():
	make_sales_order()

	for data in dataent.get_all('Sales Order', fields=["name"],
		filters = [["per_billed", "<", "100"]]):
		si = dataent.get_doc(make_sales_invoice(data.name))
		si.is_pos =1
		si.posting_date = dataent.flags.current_date
		for d in si.get("items"):
			if not d.income_account:
				d.income_account = "Sales - {}".format(dataent.get_cached_value('Company',  si.company,  'abbr'))
		si.set_missing_values()
		make_payment_entries_for_pos_invoice(si)
		si.insert()
		si.submit()

def make_payment_entries_for_pos_invoice(si):
	for data in si.payments:
		data.amount = si.outstanding_amount
		return
