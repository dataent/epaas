# Copyright (c) 2017, Dataent and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

def execute():
	if dataent.db.exists('Module Def', 'Subscription'):
		dataent.db.sql(""" delete from `tabModule Def` where name = 'Subscription'""")