# -*- coding: utf-8 -*-
# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import dataent
from dataent import _
from dataent.utils import cint
from dataent.model.document import Document

class GradingScale(Document):
	def validate(self):
		thresholds = []
		for d in self.intervals:
			if d.threshold in thresholds:
				dataent.throw(_("Treshold {0}% appears more than once".format(d.threshold)))
			else:
				thresholds.append(cint(d.threshold))
		if 0 not in thresholds:
			dataent.throw(_("Please define grade for Threshold 0%"))