# Copyright (c) 2018, Dataent and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent
from epaas.setup.doctype.company.company import install_country_fixtures

def execute():
	dataent.reload_doc('regional', 'report', 'fichier_des_ecritures_comptables_[fec]')
	for d in dataent.get_all('Company', filters = {'country': 'France'}):
		install_country_fixtures(d.name)
