# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

def execute():
	for d in dataent.db.sql("""select name from `tabAccount`
		where ifnull(master_type, '') not in ('Customer', 'Supplier', 'Employee', '') and docstatus=0"""):
			ac = dataent.get_doc("Account", d[0])
			ac.master_type = None
			ac.save()
