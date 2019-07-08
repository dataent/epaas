# Copyright (c) 2013, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doc('crm', 'doctype', 'opportunity')
	dataent.reload_doc('crm', 'doctype', 'opportunity_item')

	# all existing opportunities were with items
	dataent.db.sql("update `tabDocType` set module = 'CRM' where name='Opportunity Item'")
	dataent.db.sql("update tabOpportunity set with_items=1, title=customer_name")
	dataent.db.sql("update `tabEmail Account` set append_to='Opportunity' where append_to='Lead'")
