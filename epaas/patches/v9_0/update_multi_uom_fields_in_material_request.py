# Copyright (c) 2017, Dataent and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doctype('Material Request')
	dataent.reload_doctype('Material Request Item')

	dataent.db.sql(""" update `tabMaterial Request Item`
		set stock_uom = uom, stock_qty = qty, conversion_factor = 1.0""")