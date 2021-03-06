# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent
from epaas.controllers.trends	import get_columns,get_data

def execute(filters=None):
	if not filters: filters ={}
	data = []
	conditions = get_columns(filters, "Sales Order")
	data = get_data(filters, conditions)
	return conditions["columns"], data
