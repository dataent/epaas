# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals

import dataent

def execute():
	dataent.reload_doctype('Role')
	for dt in ("assessment", "course", "fees"):
		# 'Schools' module changed to the 'Education'
		# dataent.reload_doc("schools", "doctype", dt)
		dataent.reload_doc("education", "doctype", dt)

	for dt in ("domain", "has_domain", "domain_settings"):
		dataent.reload_doc("core", "doctype", dt)

	dataent.reload_doc('website', 'doctype', 'portal_menu_item')

	dataent.get_doc('Portal Settings').sync_menu()

	if 'schools' in dataent.get_installed_apps():
		domain = dataent.get_doc('Domain', 'Education')
		domain.setup_domain()
	else:
		domain = dataent.get_doc('Domain', 'Manufacturing')
		domain.setup_data()
		domain.setup_sidebar_items()
