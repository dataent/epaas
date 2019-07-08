# -*- coding: utf-8 -*-
# Copyright (c) 2018, Dataent Technologies Pvt. Ltd. and Contributors
# See license.txt
from __future__ import unicode_literals

import dataent
import unittest

class TestLeavePolicy(unittest.TestCase):
	def test_max_leave_allowed(self):
		random_leave_type = dataent.get_all("Leave Type", fields=["name", "max_leaves_allowed"])
		if random_leave_type:
			random_leave_type = random_leave_type[0]
			leave_type = dataent.get_doc("Leave Type", random_leave_type.name)
			old_max_leaves_allowed = leave_type.max_leaves_allowed
			leave_type.max_leaves_allowed = 2
			leave_type.save()

			leave_policy_details = {
				"doctype": "Leave Policy",
				"leave_policy_details": [{
					"leave_type": leave_type.name,
					"annual_allocation": leave_type.max_leaves_allowed + 1
				}]
			}

			self.assertRaises(dataent.ValidationError, dataent.get_doc(leave_policy_details).insert)
