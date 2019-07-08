# Copyright (c) 2017, Dataent and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

def execute():
	dataent.db.sql(""" update `tabAuto Email Report` set report = %s
		where name = %s""", ('Support Hour Distribution', 'Support Hours'))

	dataent.db.sql(""" update `tabCustom Role` set report = %s
		where report = %s""", ('Support Hour Distribution', 'Support Hours'))

	dataent.delete_doc('Report', 'Support Hours')