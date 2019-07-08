# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals

import dataent
import unittest

from epaas.accounts.party import get_due_date
from dataent.test_runner import make_test_records
from epaas.exceptions import PartyFrozen, PartyDisabled
from dataent.utils import flt
from epaas.selling.doctype.customer.customer import get_credit_limit, get_customer_outstanding
from epaas.tests.utils import create_test_contact_and_address

test_ignore = ["Price List"]
test_dependencies = ['Payment Term', 'Payment Terms Template']
test_records = dataent.get_test_records('Customer')

from six import iteritems

class TestCustomer(unittest.TestCase):
	def setUp(self):
		if not dataent.get_value('Item', '_Test Item'):
			make_test_records('Item')

	def tearDown(self):
		dataent.db.set_value("Customer", '_Test Customer', 'credit_limit', 0.0)

	def test_party_details(self):
		from epaas.accounts.party import get_party_details

		to_check = {
			'selling_price_list': None,
			'customer_group': '_Test Customer Group',
			'contact_designation': None,
			'customer_address': '_Test Address for Customer-Office',
			'contact_department': None,
			'contact_email': 'test_contact_customer@example.com',
			'contact_mobile': None,
			'sales_team': [],
			'contact_display': '_Test Contact for _Test Customer',
			'contact_person': '_Test Contact for _Test Customer-_Test Customer',
			'territory': u'_Test Territory',
			'contact_phone': '+91 0000000000',
			'customer_name': '_Test Customer'
		}

		create_test_contact_and_address()

		dataent.db.set_value("Contact", "_Test Contact for _Test Customer-_Test Customer",
			"is_primary_contact", 1)

		details = get_party_details("_Test Customer")

		for key, value in iteritems(to_check):
			self.assertEqual(value, details.get(key))

	def test_rename(self):
		# delete communication linked to these 2 customers
		for name in ("_Test Customer 1", "_Test Customer 1 Renamed"):
			dataent.db.sql("""delete from `tabCommunication`
				where communication_type='Comment' and reference_doctype=%s and reference_name=%s""",
				("Customer", name))

		# add comments
		comment = dataent.get_doc("Customer", "_Test Customer 1").add_comment("Comment", "Test Comment for Rename")

		# rename
		dataent.rename_doc("Customer", "_Test Customer 1", "_Test Customer 1 Renamed")

		# check if customer renamed
		self.assertTrue(dataent.db.exists("Customer", "_Test Customer 1 Renamed"))
		self.assertFalse(dataent.db.exists("Customer", "_Test Customer 1"))

		# test that comment gets linked to renamed doc
		self.assertEqual(dataent.db.get_value("Communication", {
			"communication_type": "Comment",
			"reference_doctype": "Customer",
			"reference_name": "_Test Customer 1 Renamed"
		}), comment.name)

		# rename back to original
		dataent.rename_doc("Customer", "_Test Customer 1 Renamed", "_Test Customer 1")

	def test_freezed_customer(self):
		make_test_records("Item")

		dataent.db.set_value("Customer", "_Test Customer", "is_frozen", 1)

		from epaas.selling.doctype.sales_order.test_sales_order import make_sales_order

		so = make_sales_order(do_not_save= True)

		self.assertRaises(PartyFrozen, so.save)

		dataent.db.set_value("Customer", "_Test Customer", "is_frozen", 0)

		so.save()

	def test_delete_customer_contact(self):
		customer = dataent.get_doc(
			get_customer_dict('_Test Customer for delete')).insert(ignore_permissions=True)

		customer.mobile_no = "8989889890"
		customer.save()
		self.assertTrue(customer.customer_primary_contact)
		dataent.delete_doc('Customer', customer.name)

	def test_disabled_customer(self):
		make_test_records("Item")

		dataent.db.set_value("Customer", "_Test Customer", "disabled", 1)

		from epaas.selling.doctype.sales_order.test_sales_order import make_sales_order

		so = make_sales_order(do_not_save=True)

		self.assertRaises(PartyDisabled, so.save)

		dataent.db.set_value("Customer", "_Test Customer", "disabled", 0)

		so.save()

	def test_duplicate_customer(self):
		dataent.db.sql("delete from `tabCustomer` where customer_name='_Test Customer 1'")

		if not dataent.db.get_value("Customer", "_Test Customer 1"):
			test_customer_1 = dataent.get_doc(
				get_customer_dict('_Test Customer 1')).insert(ignore_permissions=True)
		else:
			test_customer_1 = dataent.get_doc("Customer", "_Test Customer 1")

		duplicate_customer = dataent.get_doc(
			get_customer_dict('_Test Customer 1')).insert(ignore_permissions=True)

		self.assertEqual("_Test Customer 1", test_customer_1.name)
		self.assertEqual("_Test Customer 1 - 1", duplicate_customer.name)
		self.assertEqual(test_customer_1.customer_name, duplicate_customer.customer_name)

	def get_customer_outstanding_amount(self):
		from epaas.selling.doctype.sales_order.test_sales_order import make_sales_order
		outstanding_amt = get_customer_outstanding('_Test Customer', '_Test Company')

		# If outstanding is negative make a transaction to get positive outstanding amount
		if outstanding_amt > 0.0:
			return outstanding_amt

		item_qty = int((abs(outstanding_amt) + 200)/100)
		make_sales_order(qty=item_qty)
		return get_customer_outstanding('_Test Customer', '_Test Company')

	def test_customer_credit_limit(self):
		from epaas.stock.doctype.delivery_note.test_delivery_note import create_delivery_note
		from epaas.accounts.doctype.sales_invoice.test_sales_invoice import create_sales_invoice
		from epaas.selling.doctype.sales_order.test_sales_order import make_sales_order
		from epaas.selling.doctype.sales_order.sales_order import make_sales_invoice

		outstanding_amt = self.get_customer_outstanding_amount()
		credit_limit = get_credit_limit('_Test Customer', '_Test Company')

		if outstanding_amt <= 0.0:
			item_qty = int((abs(outstanding_amt) + 200)/100)
			make_sales_order(qty=item_qty)

		if credit_limit == 0.0:
			dataent.db.set_value("Customer", '_Test Customer', 'credit_limit', outstanding_amt - 50.0)

		# Sales Order
		so = make_sales_order(do_not_submit=True)
		self.assertRaises(dataent.ValidationError, so.submit)

		# Delivery Note
		dn = create_delivery_note(do_not_submit=True)
		self.assertRaises(dataent.ValidationError, dn.submit)

		# Sales Invoice
		si = create_sales_invoice(do_not_submit=True)
		self.assertRaises(dataent.ValidationError, si.submit)

		if credit_limit > outstanding_amt:
			dataent.db.set_value("Customer", '_Test Customer', 'credit_limit', credit_limit)

		# Makes Sales invoice from Sales Order
		so.save(ignore_permissions=True)
		si = make_sales_invoice(so.name)
		si.save(ignore_permissions=True)
		self.assertRaises(dataent.ValidationError, make_sales_order)

	def test_customer_credit_limit_on_change(self):
		outstanding_amt = self.get_customer_outstanding_amount()
		customer = dataent.get_doc("Customer", '_Test Customer')
		customer.credit_limit = flt(outstanding_amt - 100)
		self.assertRaises(dataent.ValidationError, customer.save)

	def test_customer_payment_terms(self):
		dataent.db.set_value(
			"Customer", "_Test Customer With Template", "payment_terms", "_Test Payment Term Template 3")

		due_date = get_due_date("2016-01-22", "Customer", "_Test Customer With Template")
		self.assertEqual(due_date, "2016-02-21")

		due_date = get_due_date("2017-01-22", "Customer", "_Test Customer With Template")
		self.assertEqual(due_date, "2017-02-21")

		dataent.db.set_value(
			"Customer", "_Test Customer With Template", "payment_terms", "_Test Payment Term Template 1")

		due_date = get_due_date("2016-01-22", "Customer", "_Test Customer With Template")
		self.assertEqual(due_date, "2016-02-29")

		due_date = get_due_date("2017-01-22", "Customer", "_Test Customer With Template")
		self.assertEqual(due_date, "2017-02-28")

		dataent.db.set_value("Customer", "_Test Customer With Template", "payment_terms", "")

		# No default payment term template attached
		due_date = get_due_date("2016-01-22", "Customer", "_Test Customer")
		self.assertEqual(due_date, "2016-01-22")

		due_date = get_due_date("2017-01-22", "Customer", "_Test Customer")
		self.assertEqual(due_date, "2017-01-22")


def get_customer_dict(customer_name):
	return {
		 "customer_group": "_Test Customer Group",
		 "customer_name": customer_name,
		 "customer_type": "Individual",
		 "doctype": "Customer",
		 "territory": "_Test Territory"
	}
