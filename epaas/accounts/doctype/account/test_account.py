# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import unittest
import dataent
from epaas.stock import get_warehouse_account, get_company_default_inventory_account
from epaas.accounts.doctype.account.account import update_account_number
from epaas.accounts.doctype.account.account import merge_account

class TestAccount(unittest.TestCase):
	def test_rename_account(self):
		if not dataent.db.exists("Account", "1210 - Debtors - _TC"):
			acc = dataent.new_doc("Account")
			acc.account_name = "Debtors"
			acc.parent_account = "Accounts Receivable - _TC"
			acc.account_number = "1210"
			acc.company = "_Test Company"
			acc.insert()

		account_number, account_name = dataent.db.get_value("Account", "1210 - Debtors - _TC",
			["account_number", "account_name"])
		self.assertEqual(account_number, "1210")
		self.assertEqual(account_name, "Debtors")

		new_account_number = "1211-11-4 - 6 - "
		new_account_name = "Debtors 1 - Test - "

		update_account_number("1210 - Debtors - _TC", new_account_name, new_account_number)

		new_acc = dataent.db.get_value("Account", "1211-11-4 - 6 - - Debtors 1 - Test - - _TC",
			["account_name", "account_number"], as_dict=1)

		self.assertEqual(new_acc.account_name, "Debtors 1 - Test -")
		self.assertEqual(new_acc.account_number, "1211-11-4 - 6 -")

		dataent.delete_doc("Account", "1211-11-4 - 6 - Debtors 1 - Test - - _TC")

	def test_merge_account(self):
		if not dataent.db.exists("Account", "Current Assets - _TC"):
			acc = dataent.new_doc("Account")
			acc.account_name = "Current Assets"
			acc.is_group = 1
			acc.parent_account = "Application of Funds (Assets) - _TC"
			acc.company = "_Test Company"
			acc.insert()
		if not dataent.db.exists("Account", "Securities and Deposits - _TC"):
			acc = dataent.new_doc("Account")
			acc.account_name = "Securities and Deposits"
			acc.parent_account = "Current Assets - _TC"
			acc.is_group = 1
			acc.company = "_Test Company"
			acc.insert()
		if not dataent.db.exists("Account", "Earnest Money - _TC"):
			acc = dataent.new_doc("Account")
			acc.account_name = "Earnest Money"
			acc.parent_account = "Securities and Deposits - _TC"
			acc.company = "_Test Company"
			acc.insert()
		if not dataent.db.exists("Account", "Cash In Hand - _TC"):
			acc = dataent.new_doc("Account")
			acc.account_name = "Cash In Hand"
			acc.is_group = 1
			acc.parent_account = "Current Assets - _TC"
			acc.company = "_Test Company"
			acc.insert()
		if not dataent.db.exists("Account", "Accumulated Depreciation - _TC"):
			acc = dataent.new_doc("Account")
			acc.account_name = "Accumulated Depreciation"
			acc.parent_account = "Fixed Assets - _TC"
			acc.company = "_Test Company"
			acc.insert()

		doc = dataent.get_doc("Account", "Securities and Deposits - _TC")
		parent = dataent.db.get_value("Account", "Earnest Money - _TC", "parent_account")

		self.assertEqual(parent, "Securities and Deposits - _TC")

		merge_account("Securities and Deposits - _TC", "Cash In Hand - _TC", doc.is_group, doc.root_type, doc.company)
		parent = dataent.db.get_value("Account", "Earnest Money - _TC", "parent_account")

		# Parent account of the child account changes after merging
		self.assertEqual(parent, "Cash In Hand - _TC")

		# Old account doesn't exist after merging
		self.assertFalse(dataent.db.exists("Account", "Securities and Deposits - _TC"))

		doc = dataent.get_doc("Account", "Current Assets - _TC")

		# Raise error as is_group property doesn't match
		self.assertRaises(dataent.ValidationError, merge_account, "Current Assets - _TC",\
			"Accumulated Depreciation - _TC", doc.is_group, doc.root_type, doc.company)

		doc = dataent.get_doc("Account", "Capital Stock - _TC")

		# Raise error as root_type property doesn't match
		self.assertRaises(dataent.ValidationError, merge_account, "Capital Stock - _TC",\
			"Softwares - _TC", doc.is_group, doc.root_type, doc.company)

	def test_account_sync(self):
		del dataent.local.flags["ignore_root_company_validation"]
		acc = dataent.new_doc("Account")
		acc.account_name = "Test Sync Account"
		acc.parent_account = "Temporary Accounts - _TC3"
		acc.company = "_Test Company 3"
		acc.insert()

		acc_tc_4 = dataent.db.get_value('Account', {'account_name': "Test Sync Account", "company": "_Test Company 4"})
		acc_tc_5 = dataent.db.get_value('Account', {'account_name': "Test Sync Account", "company": "_Test Company 5"})
		self.assertEqual(acc_tc_4, "Test Sync Account - _TC4")
		self.assertEqual(acc_tc_5, "Test Sync Account - _TC5")

def _make_test_records(verbose):
	from dataent.test_runner import make_test_objects

	accounts = [
		# [account_name, parent_account, is_group]
		["_Test Bank", "Bank Accounts", 0, "Bank", None],
		["_Test Bank USD", "Bank Accounts", 0, "Bank", "USD"],
		["_Test Bank EUR", "Bank Accounts", 0, "Bank", "EUR"],
		["_Test Cash", "Cash In Hand", 0, "Cash", None],

		["_Test Account Stock Expenses", "Direct Expenses", 1, None, None],
		["_Test Account Shipping Charges", "_Test Account Stock Expenses", 0, "Chargeable", None],
		["_Test Account Customs Duty", "_Test Account Stock Expenses", 0, "Tax", None],
		["_Test Account Insurance Charges", "_Test Account Stock Expenses", 0, "Chargeable", None],
		["_Test Account Stock Adjustment", "_Test Account Stock Expenses", 0, "Stock Adjustment", None],
		["_Test Employee Advance", "Current Liabilities", 0, None, None],

		["_Test Account Tax Assets", "Current Assets", 1, None, None],
		["_Test Account VAT", "_Test Account Tax Assets", 0, "Tax", None],
		["_Test Account Service Tax", "_Test Account Tax Assets", 0, "Tax", None],

		["_Test Account Reserves and Surplus", "Current Liabilities", 0, None, None],

		["_Test Account Cost for Goods Sold", "Expenses", 0, None, None],
		["_Test Account Excise Duty", "_Test Account Tax Assets", 0, "Tax", None],
		["_Test Account Education Cess", "_Test Account Tax Assets", 0, "Tax", None],
		["_Test Account S&H Education Cess", "_Test Account Tax Assets", 0, "Tax", None],
		["_Test Account CST", "Direct Expenses", 0, "Tax", None],
		["_Test Account Discount", "Direct Expenses", 0, None, None],
		["_Test Write Off", "Indirect Expenses", 0, None, None],
		["_Test Exchange Gain/Loss", "Indirect Expenses", 0, None, None],

		# related to Account Inventory Integration
		["_Test Account Stock In Hand", "Current Assets", 0, None, None],

		# fixed asset depreciation
		["_Test Fixed Asset", "Current Assets", 0, "Fixed Asset", None],
		["_Test Accumulated Depreciations", "Current Assets", 0, None, None],
		["_Test Depreciations", "Expenses", 0, None, None],
		["_Test Gain/Loss on Asset Disposal", "Expenses", 0, None, None],

		# Receivable / Payable Account
		["_Test Receivable", "Current Assets", 0, "Receivable", None],
		["_Test Payable", "Current Liabilities", 0, "Payable", None],
		["_Test Receivable USD", "Current Assets", 0, "Receivable", "USD"],
		["_Test Payable USD", "Current Liabilities", 0, "Payable", "USD"]
	]

	for company, abbr in [["_Test Company", "_TC"], ["_Test Company 1", "_TC1"]]:
		test_objects = make_test_objects("Account", [{
				"doctype": "Account",
				"account_name": account_name,
				"parent_account": parent_account + " - " + abbr,
				"company": company,
				"is_group": is_group,
				"account_type": account_type,
				"account_currency": currency
			} for account_name, parent_account, is_group, account_type, currency in accounts])

	return test_objects

def get_inventory_account(company, warehouse=None):
	account = None
	if warehouse:
		account = get_warehouse_account(dataent.get_doc("Warehouse", warehouse))
	else:
		account = get_company_default_inventory_account(company)

	return account

def create_account(**kwargs):
	account = dataent.db.get_value("Account", filters={"account_name": kwargs.get("account_name"), "company": kwargs.get("company")})
	if account:
		return account
	else:
		account = dataent.get_doc(dict(
			doctype = "Account",
			account_name = kwargs.get('account_name'),
			account_type = kwargs.get('account_type'),
			parent_account = kwargs.get('parent_account'),
			company = kwargs.get('company')
		))

		account.save()
		return account.name
