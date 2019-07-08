from __future__ import unicode_literals
import dataent
from dataent import _
from epaas.setup.setup_wizard.operations.install_fixtures import add_sale_stages

def execute():
	dataent.reload_doc('crm', 'doctype', 'sales_stage')

	dataent.local.lang = dataent.db.get_default("lang") or 'en'

	add_sale_stages()