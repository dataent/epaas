# Copyright (c) 2017, Dataent and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

def execute():
	domain = 'Agriculture'
	if not dataent.db.exists('Domain', domain):
		dataent.get_doc({
			'doctype': 'Domain',
			'domain': domain
		}).insert(ignore_permissions=True)