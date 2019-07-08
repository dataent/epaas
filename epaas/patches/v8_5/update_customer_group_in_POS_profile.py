from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doctype('POS Profile')
	customer_group = dataent.db.get_single_value('Selling Settings', 'customer_group')
	if customer_group:
		dataent.db.sql(""" update `tabPOS Profile`
			set customer_group = %s where customer_group is null """, (customer_group))