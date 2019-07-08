from __future__ import unicode_literals
import dataent

def execute():
	for doctype in ('Sales Order', 'Purchase Order', 'Sales Invoice',
		'Purchase Invoice'):
		dataent.reload_doctype(doctype)
		dataent.db.sql('''update `tab{0}` set submit_on_creation=1, notify_by_email=1
			where is_recurring=1'''.format(doctype))
		dataent.db.sql('''update `tab{0}` set notify_by_email=1
			where is_recurring=1'''.format(doctype))
		dataent.db.sql('''update `tab{0}` set recurring_id = name
			where is_recurring=1 and ifnull(recurring_id, '') = "" '''.format(doctype))
