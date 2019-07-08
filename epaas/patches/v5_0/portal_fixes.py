from __future__ import unicode_literals
import dataent
import epaas.setup.install

def execute():
	dataent.reload_doc("website", "doctype", "web_form_field", force=True, reset_permissions=True)
	#epaas.setup.install.add_web_forms()
