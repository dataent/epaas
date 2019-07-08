# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

def execute():
	for dt in ("Stock Ledger Entry", "Communication", "DefaultValue", "DocShare", "File", "ToDo"):
		dataent.get_doc("DocType", dt).run_module_method("on_doctype_update")
