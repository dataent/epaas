# -*- coding: utf-8 -*-
# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors and Contributors
# See license.txt
from __future__ import unicode_literals

import dataent
import unittest
from epaas.stock.get_item_details import get_pos_profile
from epaas.accounts.doctype.sales_invoice.pos import get_items_list, get_customers_list

class TestPOSProfile(unittest.TestCase):
	def test_pos_profile(self):
		make_pos_profile()

		pos_profile = get_pos_profile("_Test Company") or {}
		if pos_profile:
			doc = dataent.get_doc("POS Profile", pos_profile.get("name"))
			doc.append('item_groups', {'item_group': '_Test Item Group'})
			doc.append('customer_groups', {'customer_group': '_Test Customer Group'})
			doc.save()
			items = get_items_list(doc, doc.company)
			customers = get_customers_list(doc)

			products_count = dataent.db.sql(""" select count(name) from tabItem where item_group = '_Test Item Group'""", as_list=1)
			customers_count = dataent.db.sql(""" select count(name) from tabCustomer where customer_group = '_Test Customer Group'""")

			self.assertEqual(len(items), products_count[0][0])
			self.assertEqual(len(customers), customers_count[0][0])

		dataent.db.sql("delete from `tabPOS Profile`")

def make_pos_profile():
	dataent.db.sql("delete from `tabPOS Profile`")

	pos_profile = dataent.get_doc({
		"company": "_Test Company",
		"cost_center": "_Test Cost Center - _TC",
		"currency": "INR",
		"doctype": "POS Profile",
		"expense_account": "_Test Account Cost for Goods Sold - _TC",
		"income_account": "Sales - _TC",
		"name": "_Test POS Profile",
		"naming_series": "_T-POS Profile-",
		"selling_price_list": "_Test Price List",
		"territory": "_Test Territory",
		"customer_group": dataent.db.get_value('Customer Group', {'is_group': 0}, 'name'),
		"warehouse": "_Test Warehouse - _TC",
		"write_off_account": "_Test Write Off - _TC",
		"write_off_cost_center": "_Test Write Off Cost Center - _TC"
	})

	if not dataent.db.exists("POS Profile", "_Test POS Profile"):
		pos_profile.insert()

	return pos_profile
