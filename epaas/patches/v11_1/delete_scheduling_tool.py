# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

def execute():
	if dataent.db.exists("DocType", "Scheduling Tool"):
		dataent.delete_doc("DocType", "Scheduling Tool", ignore_permissions=True)
