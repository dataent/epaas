# Copyright (c) 2017, Dataent and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doc('core', 'doctype', 'has_role')
	company = dataent.get_all('Company', filters = {'country': 'India'})

	if not company:
		dataent.db.sql("""
			delete from
				`tabHas Role`
			where
				parenttype = 'Report' and parent in('GST Sales Register',
					'GST Purchase Register', 'GST Itemised Sales Register',
					'GST Itemised Purchase Register', 'Eway Bill')""")