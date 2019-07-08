# -*- coding: utf-8 -*-
# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import dataent
from dataent import _
from dataent.utils import getdate
from dataent.model.document import Document

class Vehicle(Document):
	def validate(self):
		if getdate(self.start_date) > getdate(self.end_date):
			dataent.throw(_("Insurance Start date should be less than Insurance End date"))