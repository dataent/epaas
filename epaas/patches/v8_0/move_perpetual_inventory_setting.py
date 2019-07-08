# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doctype('Company')
	enabled = dataent.db.get_single_value("Accounts Settings", "auto_accounting_for_stock") or 0
	for data in dataent.get_all('Company', fields = ["name"]):
		doc = dataent.get_doc('Company', data.name)
		doc.enable_perpetual_inventory = enabled
		doc.db_update()