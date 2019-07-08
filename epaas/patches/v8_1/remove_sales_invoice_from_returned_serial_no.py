# Copyright (c) 2017, Dataent and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doctype("Serial No")

	dataent.db.sql("""
		update
			`tabSerial No`
		set
			sales_invoice = NULL
		where
			sales_invoice in (select return_against from
				`tabSales Invoice` where docstatus =1 and is_return=1)
			and sales_invoice is not null and sales_invoice !='' """)