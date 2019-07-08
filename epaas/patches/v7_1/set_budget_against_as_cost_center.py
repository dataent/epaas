from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doc("accounts", "doctype", "budget")
	dataent.db.sql("""
		update
			`tabBudget`
		set
			budget_against = 'Cost Center'
		""")
