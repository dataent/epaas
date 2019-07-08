# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dataent Technologies Pvt. Ltd. and Contributors
# See license.txt
from __future__ import unicode_literals

import dataent
import unittest
from dataent.utils import nowdate, get_last_day, add_days
from epaas.stock.doctype.purchase_receipt.test_purchase_receipt import make_purchase_receipt
from epaas.assets.doctype.asset_maintenance.asset_maintenance import calculate_next_due_date

class TestAssetMaintenance(unittest.TestCase):
	def setUp(self):
		set_depreciation_settings_in_company()
		create_asset_data()
		create_maintenance_team()

	def test_create_asset_maintenance(self):
		pr = make_purchase_receipt(item_code="Photocopier",
			qty=1, rate=100000.0, location="Test Location")

		asset_name = dataent.db.get_value("Asset", {"purchase_receipt": pr.name}, 'name')
		asset_doc = dataent.get_doc('Asset', asset_name)
		month_end_date = get_last_day(nowdate())

		purchase_date = nowdate() if nowdate() != month_end_date else add_days(nowdate(), -15)

		asset_doc.available_for_use_date = purchase_date
		asset_doc.purchase_date = purchase_date

		asset_doc.calculate_depreciation = 1
		asset_doc.append("finance_books", {
			"expected_value_after_useful_life": 200,
			"depreciation_method": "Straight Line",
			"total_number_of_depreciations": 3,
			"frequency_of_depreciation": 10,
			"depreciation_start_date": month_end_date
		})

		asset_doc.save()

		if not dataent.db.exists("Asset Maintenance", "Photocopier"):
			asset_maintenance =	dataent.get_doc({
					"doctype": "Asset Maintenance",
					"asset_name": "Photocopier",
					"maintenance_team": "Team Awesome",
					"company": "_Test Company",
					"asset_maintenance_tasks": get_maintenance_tasks()
				}).insert()

			next_due_date = calculate_next_due_date(nowdate(), "Monthly")
			self.assertEqual(asset_maintenance.asset_maintenance_tasks[0].next_due_date, next_due_date)

	def test_create_asset_maintenance_log(self):
		if not dataent.db.exists("Asset Maintenance Log", "Photocopier"):
			asset_maintenance_log =	dataent.get_doc({
					"doctype": "Asset Maintenance Log",
					"asset_maintenance": "Photocopier",
					"task": "Change Oil",
					"completion_date": add_days(nowdate(), 2),
					"maintenance_status": "Completed"
				}).insert()
		asset_maintenance = dataent.get_doc("Asset Maintenance", "Photocopier")
		next_due_date = calculate_next_due_date(asset_maintenance_log.completion_date, "Monthly")
		self.assertEqual(asset_maintenance.asset_maintenance_tasks[0].next_due_date, next_due_date)

def create_asset_data():
	if not dataent.db.exists("Asset Category", "Equipment"):
		create_asset_category()

	if not dataent.db.exists("Location", "Test Location"):
		dataent.get_doc({
			'doctype': 'Location',
			'location_name': 'Test Location'
		}).insert()

	if not dataent.db.exists("Item", "Photocopier"):
		dataent.get_doc({
			"doctype": "Item",
			"item_code": "Photocopier",
			"item_name": "Photocopier",
			"item_group": "All Item Groups",
			"company": "_Test Company",
			"is_fixed_asset": 1,
			"is_stock_item": 0,
			"asset_category": "Equipment"
		}).insert()

def create_maintenance_team():
	user_list = ["marcus@abc.com", "thalia@abc.com", "mathias@abc.com"]
	if not dataent.db.exists("Role", "Technician"):
		dataent.get_doc({"doctype": "Role", "role_name": "Technician"}).insert()
	for user in user_list:
		if not dataent.db.get_value("User", user):
			dataent.get_doc({
				"doctype": "User",
				"email": user,
				"first_name": user,
				"new_password": "password",
				"roles": [{"doctype": "Has Role", "role": "Technician"}]
			}).insert()

	if not dataent.db.exists("Asset Maintenance Team", "Team Awesome"):
		dataent.get_doc({
			"doctype": "Asset Maintenance Team",
			"maintenance_manager": "marcus@abc.com",
			"maintenance_team_name": "Team Awesome",
			"company": "_Test Company",
			"maintenance_team_members": get_maintenance_team(user_list)
		}).insert()

def get_maintenance_team(user_list):
	return [{"team_member": user,
			"full_name": user,
			"maintenance_role": "Technician"
			}
		for user in user_list[1:]]

def get_maintenance_tasks():
	return [{"maintenance_task": "Change Oil",
			"start_date": nowdate(),
			"periodicity": "Monthly",
			"maintenance_type": "Preventive Maintenance",
			"maintenance_status": "Planned"
			},
			{"maintenance_task": "Check Gears",
			"start_date": nowdate(),
			"periodicity": "Yearly",
			"maintenance_type": "Calibration",
			"maintenance_status": "Planned"
			}
		]

def create_asset_category():
	asset_category = dataent.new_doc("Asset Category")
	asset_category.asset_category_name = "Equipment"
	asset_category.total_number_of_depreciations = 3
	asset_category.frequency_of_depreciation = 3
	asset_category.append("accounts", {
		"company_name": "_Test Company",
		"fixed_asset_account": "_Test Fixed Asset - _TC",
		"accumulated_depreciation_account": "_Test Accumulated Depreciations - _TC",
		"depreciation_expense_account": "_Test Depreciations - _TC"
	})
	asset_category.insert()

def set_depreciation_settings_in_company():
	company = dataent.get_doc("Company", "_Test Company")
	company.accumulated_depreciation_account = "_Test Accumulated Depreciations - _TC"
	company.depreciation_expense_account = "_Test Depreciations - _TC"
	company.disposal_account = "_Test Gain/Loss on Asset Disposal - _TC"
	company.depreciation_cost_center = "_Test Cost Center - _TC"
	company.save()
	
	# Enable booking asset depreciation entry automatically
	dataent.db.set_value("Accounts Settings", None, "book_asset_depreciation_entry_automatically", 1)	