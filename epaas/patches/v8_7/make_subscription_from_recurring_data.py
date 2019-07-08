# Copyright (c) 2017, Dataent and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent
from dataent.utils import today

def execute():
	dataent.reload_doc('accounts', 'doctype', 'subscription')
	dataent.reload_doc('selling', 'doctype', 'sales_order')
	dataent.reload_doc('selling', 'doctype', 'quotation')
	dataent.reload_doc('buying', 'doctype', 'purchase_order')
	dataent.reload_doc('buying', 'doctype', 'supplier_quotation')
	dataent.reload_doc('accounts', 'doctype', 'sales_invoice')
	dataent.reload_doc('accounts', 'doctype', 'purchase_invoice')
	dataent.reload_doc('stock', 'doctype', 'purchase_receipt')
	dataent.reload_doc('stock', 'doctype', 'delivery_note')
	dataent.reload_doc('accounts', 'doctype', 'journal_entry')
	dataent.reload_doc('accounts', 'doctype', 'payment_entry')

	for doctype in ['Sales Order', 'Sales Invoice', 'Purchase Order', 'Purchase Invoice']:
		date_field = "transaction_date"
		if doctype in ("Sales Invoice", "Purchase Invoice"):
			date_field = "posting_date"

		for data in get_data(doctype, date_field):
			make_subscription(doctype, data, date_field)

def get_data(doctype, date_field):
	return dataent.db.sql(""" select name, from_date, end_date, recurring_type, recurring_id,
		next_date, notify_by_email, notification_email_address, recurring_print_format,
		repeat_on_day_of_month, submit_on_creation, docstatus, {0}
		from `tab{1}` where is_recurring = 1 and next_date >= %s and docstatus < 2
		order by next_date desc
	""".format(date_field, doctype), today(), as_dict=1)

def make_subscription(doctype, data, date_field):
	if data.name == data.recurring_id:
		start_date = data.get(date_field)
	else:
		start_date = dataent.db.get_value(doctype, data.recurring_id, date_field)

	doc = dataent.get_doc({
		'doctype': 'Subscription',
		'reference_doctype': doctype,
		'reference_document': data.recurring_id,
		'start_date': start_date,
		'end_date': data.end_date,
		'frequency': data.recurring_type,
		'repeat_on_day': data.repeat_on_day_of_month,
		'notify_by_email': data.notify_by_email,
		'recipients': data.notification_email_address,
		'next_schedule_date': data.next_date,
		'submit_on_creation': data.submit_on_creation
	}).insert(ignore_permissions=True)

	if data.docstatus == 1:
		doc.submit()