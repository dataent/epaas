# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doc("accounts", "doctype", "sales_taxes_and_charges")
	docs_with_discount_amount = dataent._dict()
	for dt in ["Quotation", "Sales Order", "Delivery Note", "Sales Invoice"]:
		records = dataent.db.sql_list("""select name from `tab%s`
			where ifnull(discount_amount, 0) > 0 and docstatus=1""" % dt)
		docs_with_discount_amount[dt] = records

	for dt, discounted_records in docs_with_discount_amount.items():
		dataent.db.sql("""update `tabSales Taxes and Charges`
			set tax_amount_after_discount_amount = tax_amount
			where parenttype = %s and parent not in (%s)""" %
			('%s', ', '.join(['%s']*(len(discounted_records)+1))),
			tuple([dt, ''] + discounted_records))
