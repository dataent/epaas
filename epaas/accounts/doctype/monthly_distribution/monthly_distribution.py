# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent
from dataent.utils import flt
from dataent import _
from dataent.model.document import Document

class MonthlyDistribution(Document):
	def get_months(self):
		month_list = ['January','February','March','April','May','June','July','August','September',
		'October','November','December']
		idx =1
		for m in month_list:
			mnth = self.append('percentages')
			mnth.month = m
			mnth.percentage_allocation = 100.0/12
			mnth.idx = idx
			idx += 1

	def validate(self):
		total = sum([flt(d.percentage_allocation) for d in self.get("percentages")])

		if flt(total, 2) != 100.0:
			dataent.throw(_("Percentage Allocation should be equal to 100%") + \
				" ({0}%)".format(str(flt(total, 2))))
