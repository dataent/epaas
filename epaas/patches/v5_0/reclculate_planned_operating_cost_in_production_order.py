# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

def execute():					
	for wo in dataent.db.sql("""select name from `tabWork Order` where docstatus < 2""", as_dict=1):
		work_order = dataent.get_doc("Work Order", wo.name)
		if work_order.operations:
			work_order.flags.ignore_validate_update_after_submit = True
			work_order.calculate_time()
			work_order.save()