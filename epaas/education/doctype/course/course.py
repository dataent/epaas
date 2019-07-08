# -*- coding: utf-8 -*-
# Copyright (c) 2015, Dataent Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import dataent
from dataent.model.document import Document
from dataent import _

class Course(Document):
	def validate(self):
		self.validate_assessment_criteria()
	
	def validate_assessment_criteria(self):
		if self.assessment_criteria:
			total_weightage = 0
			for criteria in self.assessment_criteria:
				total_weightage += criteria.weightage or 0
			if total_weightage != 100:
				dataent.throw(_("Total Weightage of all Assessment Criteria must be 100%"))
