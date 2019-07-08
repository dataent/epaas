from __future__ import unicode_literals
import dataent
from dataent import _

def execute():
	dataent.reload_doc('stock', 'doctype', 'item')
	language = dataent.get_single("System Settings").language

	if language and language.startswith('en'): return

	dataent.local.lang = language

	all_domains = dataent.get_hooks("domains")

	for domain in all_domains:
		translated_domain = _(domain, lang=language)
		if dataent.db.exists("Domain", translated_domain):
			#if domain already exists merged translated_domain and domain
			merge = False
			if dataent.db.exists("Domain", domain):
				merge=True

			dataent.rename_doc("Domain", translated_domain, domain, ignore_permissions=True, merge=merge)

	domain_settings = dataent.get_single("Domain Settings")
	active_domains = [d.domain for d in domain_settings.active_domains]
	
	try:
		for domain in active_domains:
			domain = dataent.get_doc("Domain", domain)
			domain.setup_domain()

			if int(dataent.db.get_single_value('System Settings', 'setup_complete')):
				domain.setup_sidebar_items()
				domain.setup_desktop_icons()
				domain.set_default_portal_role()
	except dataent.LinkValidationError:
		pass