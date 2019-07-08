# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals

import dataent

def create_test_contact_and_address():
	dataent.db.sql('delete from tabContact')
	dataent.db.sql('delete from tabAddress')
	dataent.db.sql('delete from `tabDynamic Link`')

	dataent.get_doc(dict(
		doctype='Address',
		address_title='_Test Address for Customer',
		address_type='Office',
		address_line1='Station Road',
		city='_Test City',
		state='Test State',
		country='India',
		links = [dict(
			link_doctype='Customer',
			link_name='_Test Customer'
		)]
	)).insert()

	dataent.get_doc(dict(
		doctype='Contact',
		email_id='test_contact_customer@example.com',
		phone='+91 0000000000',
		first_name='_Test Contact for _Test Customer',
		links = [dict(
			link_doctype='Customer',
			link_name='_Test Customer'
		)]
	)).insert()
