from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doctype("Email Digest")
	dataent.db.sql("""update `tabEmail Digest` set expense_year_to_date =
		income_year_to_date""")

	if dataent.db.exists("Email Digest", "Scheduler Errors"):
		dataent.delete_doc("Email Digest", "Scheduler Errors")
