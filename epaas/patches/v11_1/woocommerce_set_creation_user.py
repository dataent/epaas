from __future__ import unicode_literals
import dataent
from dataent.utils import cint

def execute():
	dataent.reload_doc("epaas_integrations", "doctype","woocommerce_settings")
	doc = dataent.get_doc("Woocommerce Settings")

	if cint(doc.enable_sync):
		doc.creation_user = doc.modified_by
		doc.save(ignore_permissions=True)