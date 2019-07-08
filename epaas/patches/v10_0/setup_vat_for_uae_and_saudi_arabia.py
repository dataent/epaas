# Copyright (c) 2017, Dataent and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent
from epaas.setup.doctype.company.company import install_country_fixtures

def execute():
	dataent.reload_doc("accounts", "doctype", "account")
	dataent.reload_doc("accounts", "doctype", "payment_schedule")
	for d in dataent.get_all('Company',
		filters={'country': ('in', ['Saudi Arabia', 'United Arab Emirates'])}):
		install_country_fixtures(d.name)