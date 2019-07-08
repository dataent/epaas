from __future__ import unicode_literals
import dataent
from dataent import _

def execute():
	from epaas.setup.setup_wizard.operations.install_fixtures import default_lead_sources

	dataent.reload_doc('selling', 'doctype', 'lead_source')

	dataent.local.lang = dataent.db.get_default("lang") or 'en'

	for s in default_lead_sources:
		insert_lead_source(_(s))

	# get lead sources in existing forms (customized)
	# and create a document if not created
	for d in ['Lead', 'Opportunity', 'Quotation', 'Sales Order', 'Delivery Note', 'Sales Invoice']:
		sources = dataent.db.sql_list('select distinct source from `tab{0}`'.format(d))
		for s in sources:
			if s and s not in default_lead_sources:
				insert_lead_source(s)

		# remove customization for source
		for p in dataent.get_all('Property Setter', {'doc_type':d, 'field_name':'source', 'property':'options'}):
			dataent.delete_doc('Property Setter', p.name)

def insert_lead_source(s):
	if not dataent.db.exists('Lead Source', s):
		dataent.get_doc(dict(doctype='Lead Source', source_name=s)).insert()
