from __future__ import unicode_literals

import dataent

def execute():
	dataent.reload_doctype("Account")
	dataent.reload_doctype("Cost Center")
	dataent.db.sql("update tabAccount set is_group = if(group_or_ledger='Group', 1, 0)")
	dataent.db.sql("update `tabCost Center` set is_group = if(group_or_ledger='Group', 1, 0)")
