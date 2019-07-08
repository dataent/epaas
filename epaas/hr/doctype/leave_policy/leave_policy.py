# -*- coding: utf-8 -*-
# Copyright (c) 2018, Dataent Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import dataent
from dataent import _
from dataent.model.document import Document

class LeavePolicy(Document):
	def validate(self):
		if self.leave_policy_details:
			for lp_detail in self.leave_policy_details:
				max_leaves_allowed = dataent.db.get_value("Leave Type", lp_detail.leave_type, "max_leaves_allowed")
				if max_leaves_allowed > 0 and lp_detail.annual_allocation > max_leaves_allowed:
					dataent.throw(_("Maximum leave allowed in the leave type {0} is {1}").format(lp_detail.leave_type, max_leaves_allowed))
