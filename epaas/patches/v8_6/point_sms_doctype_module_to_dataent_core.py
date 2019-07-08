# Copyright (c) 2017, Dataent and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

def execute():
	dataent.db.sql('''UPDATE `tabDocType` SET module="Core" 
				WHERE name IN ("SMS Parameter", "SMS Settings");''')