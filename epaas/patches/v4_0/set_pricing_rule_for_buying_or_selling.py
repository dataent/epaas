# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doc("accounts", "doctype", "pricing_rule")
	dataent.db.sql("""update `tabPricing Rule` set selling=1 where ifnull(applicable_for, '') in
		('', 'Customer', 'Customer Group', 'Territory', 'Sales Partner', 'Campaign')""")

	dataent.db.sql("""update `tabPricing Rule` set buying=1 where ifnull(applicable_for, '') in
		('', 'Supplier', 'Supplier Type')""")
