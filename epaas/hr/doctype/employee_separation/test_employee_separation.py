# -*- coding: utf-8 -*-
# Copyright (c) 2018, Dataent Technologies Pvt. Ltd. and Contributors
# See license.txt
from __future__ import unicode_literals

import dataent
import unittest

test_dependencies = ["Employee Onboarding"]

class TestEmployeeSeparation(unittest.TestCase):
	def test_employee_separation(self):
		employee = dataent.db.get_value("Employee", {"status": "Active"})
		separation = dataent.new_doc('Employee Separation')
		separation.employee = employee
		separation.company = '_Test Company'
		separation.append('activities', {
			'activity_name': 'Deactivate Employee',
			'role': 'HR User'
		})
		separation.status = 'Pending'
		separation.insert()
		separation.submit()
		self.assertEqual(separation.docstatus, 1)
		separation.cancel()
		self.assertEqual(separation.project, "")