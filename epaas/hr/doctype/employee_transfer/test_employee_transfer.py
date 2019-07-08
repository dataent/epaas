# -*- coding: utf-8 -*-
# Copyright (c) 2018, Dataent Technologies Pvt. Ltd. and Contributors
# See license.txt
from __future__ import unicode_literals

import dataent
import unittest
from dataent.utils import getdate, add_days
from epaas.hr.doctype.employee.test_employee import make_employee

class TestEmployeeTransfer(unittest.TestCase):
	def setUp(self):
		make_employee("employee2@transfers.com")
		make_employee("employee3@transfers.com")
		dataent.db.sql("""delete from `tabEmployee Transfer`""")

	def test_submit_before_transfer_date(self):
		transfer_obj = dataent.get_doc({
			"doctype": "Employee Transfer",
			"employee": dataent.get_value("Employee", {"user_id":"employee2@transfers.com"}, "name"),
			"transfer_details" :[
				{
				"property": "Designation",
				"current": "Software Developer",
				"new": "Project Manager",
				"fieldname": "designation"
				}
			]
		})
		transfer_obj.transfer_date = add_days(getdate(), 1)
		transfer_obj.save()
		self.assertRaises(dataent.DocstatusTransitionError, transfer_obj.submit)
		transfer = dataent.get_doc("Employee Transfer", transfer_obj.name)
		transfer.transfer_date = getdate()
		transfer.submit()
		self.assertEqual(transfer.docstatus, 1)

	def test_new_employee_creation(self):
		transfer = dataent.get_doc({
			"doctype": "Employee Transfer",
			"employee": dataent.get_value("Employee", {"user_id":"employee3@transfers.com"}, "name"),
			"create_new_employee_id": 1,
			"transfer_date": getdate(),
			"transfer_details" :[
				{
				"property": "Designation",
				"current": "Software Developer",
				"new": "Project Manager",
				"fieldname": "designation"
				}
			]
		}).insert()
		transfer.submit()
		self.assertTrue(transfer.new_employee_id)
		self.assertEqual(dataent.get_value("Employee", transfer.new_employee_id, "status"), "Active")
		self.assertEqual(dataent.get_value("Employee", transfer.employee, "status"), "Left")
