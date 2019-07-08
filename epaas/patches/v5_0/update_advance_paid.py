# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

def execute():
	for dt in ("Sales Order", "Purchase Order"):
		orders_with_advance = dataent.db.sql("""select name from `tab{0}` 
			where docstatus < 2 and ifnull(advance_paid, 0) != 0""".format(dt), as_dict=1)
			
		for order in orders_with_advance:
			dataent.get_doc(dt, order.name).set_total_advance_paid()