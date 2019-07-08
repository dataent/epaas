# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

def execute():
	for si in dataent.db.sql_list("""select name
		from `tabSales Invoice`
		where ifnull(update_stock,0) = 1 and docstatus = 1 and exists(
			select name from `tabSales Invoice Item` where parent=`tabSales Invoice`.name and
				ifnull(so_detail, "") != "")"""):

		invoice = dataent.get_doc("Sales Invoice", si)
		invoice.update_qty()
