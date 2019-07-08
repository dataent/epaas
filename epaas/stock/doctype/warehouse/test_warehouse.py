# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt
from __future__ import unicode_literals
from dataent.model.rename_doc import rename_doc
from epaas.stock.doctype.stock_entry.stock_entry_utils import make_stock_entry
from dataent.utils import cint
from epaas import set_perpetual_inventory
from dataent.test_runner import make_test_records
from epaas.accounts.doctype.account.test_account import get_inventory_account, create_account

import epaas
import dataent
import unittest
test_records = dataent.get_test_records('Warehouse')

class TestWarehouse(unittest.TestCase):
	def setUp(self):
		if not dataent.get_value('Item', '_Test Item'):
			make_test_records('Item')

	def test_parent_warehouse(self):
		parent_warehouse = dataent.get_doc("Warehouse", "_Test Warehouse Group - _TC")
		self.assertEqual(parent_warehouse.is_group, 1)

	def test_warehouse_hierarchy(self):
		p_warehouse = dataent.get_doc("Warehouse", "_Test Warehouse Group - _TC")

		child_warehouses =  dataent.db.sql("""select name, is_group, parent_warehouse from `tabWarehouse` wh
			where wh.lft > %s and wh.rgt < %s""", (p_warehouse.lft, p_warehouse.rgt), as_dict=1)

		for child_warehouse in child_warehouses:
			self.assertEqual(p_warehouse.name, child_warehouse.parent_warehouse)
			self.assertEqual(child_warehouse.is_group, 0)

	def test_warehouse_renaming(self):
		set_perpetual_inventory(1)
		create_warehouse("Test Warehouse for Renaming 1")
		account = get_inventory_account("_Test Company", "Test Warehouse for Renaming 1 - _TC")
		self.assertTrue(dataent.db.get_value("Warehouse", filters={"account": account}))

		# Rename with abbr
		if dataent.db.exists("Warehouse", "Test Warehouse for Renaming 2 - _TC"):
			dataent.delete_doc("Warehouse", "Test Warehouse for Renaming 2 - _TC")
		rename_doc("Warehouse", "Test Warehouse for Renaming 1 - _TC", "Test Warehouse for Renaming 2 - _TC")

		self.assertTrue(dataent.db.get_value("Warehouse",
			filters={"account": "Test Warehouse for Renaming 1 - _TC"}))

		# Rename without abbr
		if dataent.db.exists("Warehouse", "Test Warehouse for Renaming 3 - _TC"):
			dataent.delete_doc("Warehouse", "Test Warehouse for Renaming 3 - _TC")

		rename_doc("Warehouse", "Test Warehouse for Renaming 2 - _TC", "Test Warehouse for Renaming 3")

		self.assertTrue(dataent.db.get_value("Warehouse",
			filters={"account": "Test Warehouse for Renaming 1 - _TC"}))

		# Another rename with multiple dashes
		if dataent.db.exists("Warehouse", "Test - Warehouse - Company - _TC"):
			dataent.delete_doc("Warehouse", "Test - Warehouse - Company - _TC")
		rename_doc("Warehouse", "Test Warehouse for Renaming 3 - _TC", "Test - Warehouse - Company")

	def test_warehouse_merging(self):
		set_perpetual_inventory(1)

		create_warehouse("Test Warehouse for Merging 1")
		create_warehouse("Test Warehouse for Merging 2")

		make_stock_entry(item_code="_Test Item", target="Test Warehouse for Merging 1 - _TC",
			qty=1, rate=100)
		make_stock_entry(item_code="_Test Item", target="Test Warehouse for Merging 2 - _TC",
			qty=1, rate=100)

		existing_bin_qty = (
			cint(dataent.db.get_value("Bin",
				{"item_code": "_Test Item", "warehouse": "Test Warehouse for Merging 1 - _TC"}, "actual_qty"))
			+ cint(dataent.db.get_value("Bin",
				{"item_code": "_Test Item", "warehouse": "Test Warehouse for Merging 2 - _TC"}, "actual_qty"))
		)

		rename_doc("Warehouse", "Test Warehouse for Merging 1 - _TC",
			"Test Warehouse for Merging 2 - _TC", merge=True)

		self.assertFalse(dataent.db.exists("Warehouse", "Test Warehouse for Merging 1 - _TC"))

		bin_qty = dataent.db.get_value("Bin",
			{"item_code": "_Test Item", "warehouse": "Test Warehouse for Merging 2 - _TC"}, "actual_qty")

		self.assertEqual(bin_qty, existing_bin_qty)

		self.assertTrue(dataent.db.get_value("Warehouse",
			filters={"account": "Test Warehouse for Merging 2 - _TC"}))

def create_warehouse(warehouse_name, properties=None, company=None):
	if not company:
		company = "_Test Company"

	warehouse_id = epaas.encode_company_abbr(warehouse_name, company)
	if not dataent.db.exists("Warehouse", warehouse_id):
		w = dataent.new_doc("Warehouse")
		w.warehouse_name = warehouse_name
		w.parent_warehouse = "_Test Warehouse Group - _TC"
		w.company = company
		make_account_for_warehouse(warehouse_name, w)
		w.account = warehouse_id
		if properties:
			w.update(properties)
		w.save()
		return w.name
	else:
		return warehouse_id

def make_account_for_warehouse(warehouse_name, warehouse_obj):
	if not dataent.db.exists("Account", warehouse_name + " - _TC"):
		parent_account = dataent.db.get_value('Account',
			{'company': warehouse_obj.company, 'is_group':1, 'account_type': 'Stock'},'name')
		account = create_account(account_name=warehouse_name, \
				account_type="Stock", parent_account= parent_account, company=warehouse_obj.company)