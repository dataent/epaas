# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent
from epaas.stock.stock_balance import update_bin_qty, get_reserved_qty

def execute():
	""" Set the Serial Numbers in Sales Invoice Item from Delivery Note Item """

	dataent.reload_doc("stock", "doctype", "serial_no")

	dataent.db.sql(""" update `tabSales Invoice Item` sii inner join 
		`tabDelivery Note Item` dni on sii.dn_detail=dni.name and  sii.qty=dni.qty
		set sii.serial_no=dni.serial_no where sii.parent IN (select si.name 
			from `tabSales Invoice` si where si.update_stock=0 and si.docstatus=1)""")

	items = dataent.db.sql(""" select  sii.parent, sii.serial_no from  `tabSales Invoice Item` sii
		left join `tabSales Invoice` si on sii.parent=si.name
		where si.docstatus=1 and si.update_stock=0""", as_dict=True)

	for item in items:
		sales_invoice = item.get("parent", None)
		serial_nos = item.get("serial_no", "")

		if not sales_invoice or not serial_nos:
			continue

		serial_nos = ["'%s'"%dataent.db.escape(no) for no in serial_nos.split("\n")]

		dataent.db.sql("""
			UPDATE 
				`tabSerial No`
			SET 
				sales_invoice='{sales_invoice}'
			WHERE
				name in ({serial_nos})
			""".format(
				sales_invoice=dataent.db.escape(sales_invoice),
				serial_nos=",".join(serial_nos)
			)
		)