# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dataent Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from dataent.model.document import Document

class MedicalCode(Document):
	def autoname(self):
		self.name = self.medical_code_standard+" "+self.code
