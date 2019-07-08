# Copyright (c) 2013, Dataent Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import dataent
from dataent import _
from epaas.projects.report.billing_summary import get_columns, get_data

def execute(filters=None):
	filters = dataent._dict(filters or {})
	columns = get_columns()

	data = get_data(filters)
	return columns, data