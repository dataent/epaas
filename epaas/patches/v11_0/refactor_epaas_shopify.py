from __future__ import unicode_literals
import dataent
from dataent.installer import remove_from_installed_apps

def execute():
	dataent.reload_doc('epaas_integrations', 'doctype', 'shopify_settings')
	dataent.reload_doc('epaas_integrations', 'doctype', 'shopify_tax_account')
	dataent.reload_doc('epaas_integrations', 'doctype', 'shopify_log')
	dataent.reload_doc('epaas_integrations', 'doctype', 'shopify_webhook_detail')

	if 'epaas_shopify' in dataent.get_installed_apps():
		remove_from_installed_apps('epaas_shopify')

		dataent.db.sql('delete from `tabDesktop Icon` where app="epaas_shopify" ')
		dataent.delete_doc("Module Def", 'epaas_shopify')

		dataent.db.commit()

		dataent.db.sql("truncate `tabShopify Log`")

		setup_app_type()
	else:
		disable_shopify()

def setup_app_type():
	try:
		shopify_settings = dataent.get_doc("Shopify Settings")
		shopify_settings.app_type = 'Private'
		shopify_settings.update_price_in_epaas_price_list = 0 if getattr(shopify_settings, 'push_prices_to_shopify', None) else 1
		shopify_settings.flags.ignore_mandatory = True
		shopify_settings.ignore_permissions = True
		shopify_settings.save()
	except Exception:
		dataent.db.set_value("Shopify Settings", None, "enable_shopify", 0)
		dataent.log_error(dataent.get_traceback())

def disable_shopify():
	# due to dataent.db.set_value wrongly written and enable_shopify being default 1
	# Shopify Settings isn't properly configured and leads to error
	shopify = dataent.get_doc('Shopify Settings')

	if shopify.app_type == "Public" or shopify.app_type == None or \
		(shopify.enable_shopify and not (shopify.shopify_url or shopify.api_key)):
		dataent.db.set_value("Shopify Settings", None, "enable_shopify", 0)
