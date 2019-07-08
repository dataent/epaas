# -*- coding: utf-8 -*-
# Copyright (c) 2015, ESS LLP and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import dataent
from dataent.model.document import Document

class PatientMedicalRecord(Document):
	def after_insert(self):
		if self.reference_doctype == "Patient Medical Record" :
			dataent.db.set_value("Patient Medical Record", self.name, "reference_name", self.name)
