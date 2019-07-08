# -*- coding: utf-8 -*-
# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import dataent
from dataent import _
from dataent.model.document import Document

STD_CRITERIA = ["total", "total score", "total grade", "maximum score", "score", "grade"]

class AssessmentCriteria(Document):
	def validate(self):
		if self.assessment_criteria.lower() in STD_CRITERIA:
			dataent.throw(_("Can't create standard criteria. Please rename the criteria"))