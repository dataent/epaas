# -*- coding: utf-8 -*-
# Copyright (c) 2018, Dataent Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import dataent
from dataent import _
from dataent.model.document import Document
from dataent.utils import getdate
from epaas.hr.utils import update_employee

class EmployeePromotion(Document):
	def validate(self):
		if dataent.get_value("Employee", self.employee, "status") == "Left":
			dataent.throw(_("Cannot promote Employee with status Left"))

	def before_submit(self):
		if getdate(self.promotion_date) > getdate():
			dataent.throw(_("Employee Promotion cannot be submitted before Promotion Date "),
				dataent.DocstatusTransitionError)

	def on_submit(self):
		employee = dataent.get_doc("Employee", self.employee)
		employee = update_employee(employee, self.promotion_details, date=self.promotion_date)
		employee.save()

	def on_cancel(self):
		employee = dataent.get_doc("Employee", self.employee)
		employee = update_employee(employee, self.promotion_details, cancel=True)
		employee.save()
