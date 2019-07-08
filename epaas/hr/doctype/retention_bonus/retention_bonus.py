# -*- coding: utf-8 -*-
# Copyright (c) 2018, Dataent Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import dataent
from dataent.model.document import Document
from dataent import _
from dataent.utils import getdate

class RetentionBonus(Document):
	def validate(self):
		if dataent.get_value("Employee", self.employee, "status") == "Left":
			dataent.throw(_("Cannot create Retention Bonus for left Employees"))
		if getdate(self.bonus_payment_date) < getdate():
			dataent.throw(_("Bonus Payment Date cannot be a past date"))
