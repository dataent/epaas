# -*- coding: utf-8 -*-
# Copyright (c) 2018, Dataent Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import dataent
from dataent import _
from dataent.utils import flt
from dataent.model.document import Document

class EmployeeTaxExemptionSubCategory(Document):
	def validate(self):
		category_max_amount = dataent.db.get_value("Employee Tax Exemption Category", self.exemption_category, "max_amount")
		if flt(self.max_amount) > flt(category_max_amount):
			dataent.throw(_("Max Exemption Amount cannot be greater than maximum exemption amount {0} of Tax Exemption Category {1}")
				.format(category_max_amount, self.exemption_category))