# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

def execute():
	dataent.db.sql("""Update `tabAccount` set account_type = 'Temporary' 
		where account_name in ('Temporary Assets', 'Temporary Liabilities', 'Temporary Opening')""")