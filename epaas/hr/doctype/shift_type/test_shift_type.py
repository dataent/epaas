# -*- coding: utf-8 -*-
# Copyright (c) 2018, Dataent Technologies Pvt. Ltd. and Contributors
# See license.txt
from __future__ import unicode_literals

import dataent
import unittest

class TestShiftType(unittest.TestCase):
	def test_make_shift_type(self):
		if dataent.db.exists("Shift Type", "Day Shift"):
			return
		shift_type = dataent.get_doc({
			"doctype": "Shift Type",
			"name": "Day Shift",
			"start_time": "9:00:00",
			"end_time": "18:00:00"
		})
		shift_type.insert()
 