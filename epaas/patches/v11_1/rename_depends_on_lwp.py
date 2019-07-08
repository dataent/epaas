# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent
from dataent import scrub
from dataent.model.utils.rename_field import rename_field

def execute():
	for doctype in ("Salary Component", "Salary Detail"):
		if "depends_on_lwp" in dataent.db.get_table_columns(doctype):
			dataent.reload_doc("hr", "doctype", scrub(doctype))
			rename_field(doctype, "depends_on_lwp", "depends_on_payment_days")