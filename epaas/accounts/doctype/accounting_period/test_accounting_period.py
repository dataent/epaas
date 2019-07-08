# -*- coding: utf-8 -*-
# Copyright (c) 2018, Dataent Technologies Pvt. Ltd. and Contributors
# See license.txt
from __future__ import unicode_literals

import dataent
import unittest

# class TestAccountingPeriod(unittest.TestCase):
# 	def test_overlap(self):
# 		ap1 = create_accounting_period({"start_date":"2018-04-01", "end_date":"2018-06-30", "company":"Wind Power LLC"})
# 		ap1.save()
# 		ap2 = create_accounting_period({"start_date":"2018-06-30", "end_date":"2018-07-10", "company":"Wind Power LLC"})
# 		self.assertRaises(dataent.OverlapError, accounting_period_2.save())
#
# 	def tearDown(self):
# 		pass
#
#
# def create_accounting_period(**args):
# 	accounting_period = dataent.new_doc("Accounting Period")
# 	accounting_period.start_date = args.start_date or dataent.utils.datetime.date(2018, 4, 1)
# 	accounting_period.end_date = args.end_date or dataent.utils.datetime.date(2018, 6, 30)
# 	accounting_period.company = args.company
# 	accounting_period.period_name = "_Test_Period_Name_1"
#
# 	return accounting_period
