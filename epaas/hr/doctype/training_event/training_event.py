# -*- coding: utf-8 -*-
# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import dataent
from dataent.model.document import Document
from dataent import _
from dataent.utils import time_diff_in_seconds
from epaas.hr.doctype.employee.employee import get_employee_emails

class TrainingEvent(Document):
	def validate(self):
		self.set_employee_emails()
		self.validate_period()

	def set_employee_emails(self):
		self.employee_emails = ', '.join(get_employee_emails([d.employee
			for d in self.employees]))

	def validate_period(self):
		if time_diff_in_seconds(self.end_time, self.start_time) <= 0:
			dataent.throw(_('End time cannot be before start time'))