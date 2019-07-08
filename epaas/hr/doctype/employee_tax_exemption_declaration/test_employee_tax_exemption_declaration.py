# -*- coding: utf-8 -*-
# Copyright (c) 2018, Dataent Technologies Pvt. Ltd. and Contributors
# See license.txt
from __future__ import unicode_literals

import dataent, epaas
import unittest
from epaas.hr.doctype.employee.test_employee import make_employee
from epaas.hr.doctype.employee_tax_exemption_declaration.employee_tax_exemption_declaration import DuplicateDeclarationError

class TestEmployeeTaxExemptionDeclaration(unittest.TestCase):
	def setUp(self):
		make_employee("employee@taxexepmtion.com")
		make_employee("employee1@taxexepmtion.com")
		create_payroll_period()
		create_exemption_category()
		dataent.db.sql("""delete from `tabEmployee Tax Exemption Declaration`""")

	def test_duplicate_category_in_declaration(self):
		declaration = dataent.get_doc({
			"doctype": "Employee Tax Exemption Declaration",
			"employee": dataent.get_value("Employee", {"user_id":"employee@taxexepmtion.com"}, "name"),
			"company": epaas.get_default_company(),
			"payroll_period": "_Test Payroll Period",
			"declarations": [
				dict(exemption_sub_category = "_Test Sub Category",
					exemption_category = "_Test Category",
					amount = 100000),
				dict(exemption_sub_category = "_Test Sub Category",
					exemption_category = "_Test Category",
					amount = 50000)
			]
		})
		self.assertRaises(dataent.ValidationError, declaration.save)

	def test_duplicate_entry_for_payroll_period(self):
		declaration = dataent.get_doc({
			"doctype": "Employee Tax Exemption Declaration",
			"employee": dataent.get_value("Employee", {"user_id":"employee@taxexepmtion.com"}, "name"),
			"company":  epaas.get_default_company(),
			"payroll_period": "_Test Payroll Period",
			"declarations": [
				dict(exemption_sub_category = "_Test Sub Category",
					exemption_category = "_Test Category",
					amount = 100000),
				dict(exemption_sub_category = "_Test1 Sub Category",
					exemption_category = "_Test Category",
					amount = 50000),
			]
		}).insert()

		duplicate_declaration = dataent.get_doc({
			"doctype": "Employee Tax Exemption Declaration",
			"employee": dataent.get_value("Employee", {"user_id":"employee@taxexepmtion.com"}, "name"),
			"company":  epaas.get_default_company(),
			"payroll_period": "_Test Payroll Period",
			"declarations": [
				dict(exemption_sub_category = "_Test Sub Category",
					exemption_category = "_Test Category",
					amount = 100000)
			]
		})
		self.assertRaises(DuplicateDeclarationError, duplicate_declaration.insert)
		duplicate_declaration.employee = dataent.get_value("Employee", {"user_id":"employee1@taxexepmtion.com"}, "name")
		self.assertTrue(duplicate_declaration.insert)

	def test_exemption_amount(self):
		declaration = dataent.get_doc({
			"doctype": "Employee Tax Exemption Declaration",
			"employee": dataent.get_value("Employee", {"user_id":"employee@taxexepmtion.com"}, "name"),
			"company":  epaas.get_default_company(),
			"payroll_period": "_Test Payroll Period",
			"declarations": [
				dict(exemption_sub_category = "_Test Sub Category",
					exemption_category = "_Test Category",
					amount = 80000),
				dict(exemption_sub_category = "_Test1 Sub Category",
					exemption_category = "_Test Category",
					amount = 60000),
			]
		}).insert()

		self.assertEqual(declaration.total_exemption_amount, 100000)

def create_payroll_period():
	if not dataent.db.exists("Payroll Period", "_Test Payroll Period"):
		from datetime import date
		payroll_period = dataent.get_doc(dict(
			doctype = 'Payroll Period',
			name = "_Test Payroll Period",
			company =  epaas.get_default_company(),
			start_date = date(date.today().year, 1, 1),
			end_date = date(date.today().year, 12, 31)
		)).insert()
		return payroll_period
	else:
		return dataent.get_doc("Payroll Period", "_Test Payroll Period")

def create_exemption_category():
	if not dataent.db.exists("Employee Tax Exemption Category", "_Test Category"):
		category = dataent.get_doc({
			"doctype": "Employee Tax Exemption Category",
			"name": "_Test Category",
			"deduction_component": "Income Tax",
			"max_amount": 100000
		}).insert()
	if not dataent.db.exists("Employee Tax Exemption Sub Category", "_Test Sub Category"):
		dataent.get_doc({
			"doctype": "Employee Tax Exemption Sub Category",
			"name": "_Test Sub Category",
			"exemption_category": "_Test Category",
			"max_amount": 100000,
			"is_active": 1
		}).insert()
	if not dataent.db.exists("Employee Tax Exemption Sub Category", "_Test1 Sub Category"):
		dataent.get_doc({
			"doctype": "Employee Tax Exemption Sub Category",
			"name": "_Test1 Sub Category",
			"exemption_category": "_Test Category",
			"max_amount": 50000,
			"is_active": 1
		}).insert()
