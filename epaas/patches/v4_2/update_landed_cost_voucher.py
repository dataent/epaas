# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doc("stock", "doctype", "landed_cost_voucher")
	dataent.db.sql("""update `tabLanded Cost Voucher` set distribute_charges_based_on = 'Amount'
		where docstatus=1""")
