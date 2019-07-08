# Copyright (c) 2017, Dataent and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doctype("Portal Settings")

	dataent.db.sql("""
		delete from
			`tabPortal Menu Item`
		where
			(route = '/quotations' and title = 'Supplier Quotation')
		or (route = '/quotation' and title = 'Quotations')
	""")