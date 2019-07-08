# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors

from __future__ import unicode_literals
import dataent

def execute():
	hr = dataent.db.get_value("Module Def", "HR")
	if hr == "Hr":
		dataent.rename_doc("Module Def", "Hr", "HR")
		dataent.db.set_value("Module Def", "HR", "module_name", "HR")

	dataent.clear_cache()
	dataent.setup_module_map()
