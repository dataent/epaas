from __future__ import unicode_literals
from dataent import _

def get_data():
	return {
		'fieldname': 'prevdoc_docname',
		'non_standard_fieldnames': {
			'Auto Repeat': 'reference_document',
		},
		'transactions': [
			{
				'label': _('Sales Order'),
				'items': ['Sales Order']
			},
			{
				'label': _('Subscription'),
				'items': ['Auto Repeat']
			},
		]
	}