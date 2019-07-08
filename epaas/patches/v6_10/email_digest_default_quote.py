from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doctype("Email Digest")
	dataent.db.sql("update `tabEmail Digest` set add_quote = 1")
