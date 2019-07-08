# Copyright (c) 2013, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doctype("Time Log")
	for d in dataent.get_all("Time Log"):
		time_log = dataent.get_doc("Time Log", d.name)
		time_log.set_title()
		dataent.db.set_value("Time Log", time_log.name, "title", time_log.title)
