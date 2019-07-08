# Copyright (c) 2013, Dataent Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from epaas.selling.report.sales_analytics.sales_analytics import Analytics

def execute(filters=None):
	return Analytics(filters).run()
