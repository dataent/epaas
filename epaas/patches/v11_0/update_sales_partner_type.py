from __future__ import unicode_literals
import dataent
from dataent import _

def execute():
	from epaas.setup.setup_wizard.operations.install_fixtures import default_sales_partner_type

	dataent.reload_doc('selling', 'doctype', 'sales_partner_type')

	dataent.local.lang = dataent.db.get_default("lang") or 'en'

	for s in default_sales_partner_type:
		insert_sales_partner_type(_(s))

	# get partner type in existing forms (customized)
	# and create a document if not created
	for d in ['Sales Partner']:
		partner_type = dataent.db.sql_list('select distinct partner_type from `tab{0}`'.format(d))
		for s in partner_type:
			if s and s not in default_sales_partner_type:
				insert_sales_partner_type(s)

		# remove customization for partner type
		for p in dataent.get_all('Property Setter', {'doc_type':d, 'field_name':'partner_type', 'property':'options'}):
			dataent.delete_doc('Property Setter', p.name)

def insert_sales_partner_type(s):
	if not dataent.db.exists('Sales Partner Type', s):
		dataent.get_doc(dict(doctype='Sales Partner Type', sales_partner_type=s)).insert()
