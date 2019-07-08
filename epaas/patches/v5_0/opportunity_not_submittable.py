# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doctype("Opportunity")
	dataent.db.sql("update tabDocPerm set submit=0, cancel=0, amend=0 where parent='Opportunity'")
	dataent.db.sql("update tabOpportunity set docstatus=0 where docstatus=1")
