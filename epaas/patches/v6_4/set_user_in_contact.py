from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doctype("Contact")
	dataent.db.sql("""update tabContact, tabUser set tabContact.user = tabUser.name
		where tabContact.email_id = tabUser.email""")
