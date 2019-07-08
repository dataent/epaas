# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

def execute():
	doctypes = dataent.db.sql(""" select name, autoname from `tabDocType`
		where autoname like 'field:%' and allow_rename = 1""", as_dict=1)

	for doctype in doctypes:
		fieldname = doctype.autoname.split(":")[1]
		if fieldname:
			dataent.db.sql(""" update `tab%s` set %s = name """%(doctype.name, fieldname))