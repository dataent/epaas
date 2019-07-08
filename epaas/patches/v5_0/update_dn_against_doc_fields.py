# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doc('stock', 'doctype', 'delivery_note_item')

	dataent.db.sql("""update `tabDelivery Note Item` set so_detail = prevdoc_detail_docname
		where ifnull(against_sales_order, '') != ''""")

	dataent.db.sql("""update `tabDelivery Note Item` set si_detail = prevdoc_detail_docname
		where ifnull(against_sales_invoice, '') != ''""")
