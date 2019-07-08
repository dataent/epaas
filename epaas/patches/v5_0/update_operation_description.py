# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent
import dataent.permissions

def execute():
	if "opn_description" in dataent.db.get_table_columns("BOM Operation"):
		dataent.db.sql("""update `tabBOM Operation` set description = opn_description
			where ifnull(description, '') = ''""")