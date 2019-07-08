# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doc("manufacturing", "doctype", "bom")
	company = dataent.db.get_value("Global Defaults", None, "default_company")
	dataent.db.sql("""update  `tabBOM` set company = %s""",company)
