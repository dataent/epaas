# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

def execute():
	if dataent.db.exists('Module Def', 'Fleet Management'):
		dataent.db.sql("""delete from `tabModule Def`
			where module_name = 'Fleet Management'""")