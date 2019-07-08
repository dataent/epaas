# -*- coding: utf-8 -*-
# Copyright (c) 2018, Dataent Technologies Pvt. Ltd. and Contributors
# See license.txt
from __future__ import unicode_literals

import dataent
import unittest


class TestCashFlowMapping(unittest.TestCase):
	def setUp(self):
		if dataent.db.exists("Cash Flow Mapping", "Test Mapping"):
			dataent.delete_doc('Cash Flow Mappping', 'Test Mapping')

	def tearDown(self):
		dataent.delete_doc('Cash Flow Mapping', 'Test Mapping')

	def test_multiple_selections_not_allowed(self):
		doc = dataent.new_doc('Cash Flow Mapping')
		doc.mapping_name = 'Test Mapping'
		doc.label = 'Test label'
		doc.append(
			'accounts',
			{'account': 'Accounts Receivable - _TC'}
		)
		doc.is_working_capital = 1
		doc.is_finance_cost = 1

		self.assertRaises(dataent.ValidationError, doc.insert)

		doc.is_finance_cost = 0
		doc.insert()
