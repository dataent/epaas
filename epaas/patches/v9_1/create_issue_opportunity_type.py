# Copyright (c) 2017, Dataent and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent
from dataent import _

def execute():
	# delete custom field if exists
	for doctype, fieldname in (('Issue', 'issue_type'), ('Opportunity', 'opportunity_type')):
		custom_field = dataent.db.get_value("Custom Field", {"fieldname": fieldname, 'dt': doctype})
		if custom_field:
			dataent.delete_doc("Custom Field", custom_field, ignore_permissions=True)

	dataent.reload_doc('support', 'doctype', 'issue_type')
	dataent.reload_doc('support', 'doctype', 'issue')
	dataent.reload_doc('crm', 'doctype', 'opportunity_type')
	dataent.reload_doc('crm', 'doctype', 'opportunity')

	# rename enquiry_type -> opportunity_type
	from dataent.model.utils.rename_field import rename_field
	rename_field('Opportunity', 'enquiry_type', 'opportunity_type')

	# create values if already set
	for opts in (('Issue', 'issue_type', 'Issue Type'),
		('Opportunity', 'opportunity_type', 'Opportunity Type')):
		for d in dataent.db.sql('select distinct {0} from `tab{1}`'.format(opts[1], opts[0])):
			if d[0] and not dataent.db.exists(opts[2], d[0]):
				dataent.get_doc(dict(doctype = opts[2], name=d[0])).insert()

	# fixtures
	for name in ('Hub', _('Sales'), _('Support'), _('Maintenance')):
		if not dataent.db.exists('Opportunity Type', name):
			dataent.get_doc(dict(doctype = 'Opportunity Type', name=name)).insert()
