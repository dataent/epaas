# -*- coding: utf-8 -*-
# Copyright (c) 2018, Dataent Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from epaas.hr.utils import EmployeeBoardingController

class EmployeeSeparation(EmployeeBoardingController):
	def validate(self):
		super(EmployeeSeparation, self).validate()

	def on_submit(self):
		super(EmployeeSeparation, self).on_submit()
	
	def on_cancel(self):
		super(EmployeeSeparation, self).on_cancel()