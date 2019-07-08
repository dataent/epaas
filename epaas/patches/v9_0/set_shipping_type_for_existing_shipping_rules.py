# Copyright (c) 2017, Dataent and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doctype("Shipping Rule")

	# default "calculate_based_on"
	dataent.db.sql('''update `tabShipping Rule`
		set calculate_based_on = "Net Weight"
		where ifnull(calculate_based_on, '') = '' ''')

	# default "shipping_rule_type"
	dataent.db.sql('''update `tabShipping Rule`
		set shipping_rule_type = "Selling"
		where ifnull(shipping_rule_type, '') = '' ''')
