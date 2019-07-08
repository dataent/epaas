from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doctype("System Settings")
	ss = dataent.get_doc("System Settings", "System Settings")
	ss.email_footer_address = dataent.db.get_default("company")
	ss.flags.ignore_mandatory = True
	ss.save()
