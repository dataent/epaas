# Copyright (c) 2017, Dataent and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doc('accounts', 'doctype', 'purchase_invoice_item')
	dataent.db.sql("update `tabPurchase Invoice Item` set stock_qty = qty, stock_uom = uom")