# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent, epaas

from dataent import _
from six import iteritems

def get_level():

	activation_level = 0
	sales_data = []
	min_count = 0
	doctypes = {"Item": 5, "Customer": 5, "Sales Order": 2, "Sales Invoice": 2, "Purchase Order": 2, "Employee": 3, "Lead": 3, "Quotation": 3,
					"Payment Entry": 2, "User": 5, "Student": 5, "Instructor": 5, "BOM": 3, "Journal Entry": 3, "Stock Entry": 3}
	for doctype, min_count in iteritems(doctypes):
		count = dataent.db.count(doctype)
		if count > min_count:
			activation_level += 1
		sales_data.append({doctype: count})

	if dataent.db.get_single_value('System Settings', 'setup_complete'):
		activation_level += 1

	communication_number = dataent.db.count('Communication', dict(communication_medium='Email'))
	if communication_number > 10:
		activation_level += 1
	sales_data.append({"Communication": communication_number})

	# recent login
	if dataent.db.sql('select name from tabUser where last_login > date_sub(now(), interval 2 day) limit 1'):
		activation_level += 1

	level = {"activation_level": activation_level, "sales_data": sales_data}

	return level

def get_help_messages():
	'''Returns help messages to be shown on Desktop'''
	if get_level() > 6:
		return []

	domain = dataent.get_cached_value('Company',  epaas.get_default_company(),  'domain')
	messages = []

	message_settings = [
		dataent._dict(
			doctype='Lead',
			title=_('Create Leads'),
			description=_('Leads help you get business, add all your contacts and more as your leads'),
			action=_('Make Lead'),
			route='List/Lead',
			domain=('Manufacturing', 'Retail', 'Services', 'Distribution'),
			target=3
		),
		dataent._dict(
			doctype='Quotation',
			title=_('Create customer quotes'),
			description=_('Quotations are proposals, bids you have sent to your customers'),
			action=_('Make Quotation'),
			route='List/Quotation',
			domain=('Manufacturing', 'Retail', 'Services', 'Distribution'),
			target=3
		),
		dataent._dict(
			doctype='Sales Order',
			title=_('Manage your orders'),
			description=_('Make Sales Orders to help you plan your work and deliver on-time'),
			action=_('Make Sales Order'),
			route='List/Sales Order',
			domain=('Manufacturing', 'Retail', 'Services', 'Distribution'),
			target=3
		),
		dataent._dict(
			doctype='Purchase Order',
			title=_('Create Purchase Orders'),
			description=_('Purchase orders help you plan and follow up on your purchases'),
			action=_('Make Purchase Order'),
			route='List/Purchase Order',
			domain=('Manufacturing', 'Retail', 'Services', 'Distribution'),
			target=3
		),
		dataent._dict(
			doctype='User',
			title=_('Create Users'),
			description=_('Add the rest of your organization as your users. You can also add invite Customers to your portal by adding them from Contacts'),
			action=_('Make User'),
			route='List/User',
			domain=('Manufacturing', 'Retail', 'Services', 'Distribution'),
			target=3
		),
		dataent._dict(
			doctype='Timesheet',
			title=_('Add Timesheets'),
			description=_('Timesheets help keep track of time, cost and billing for activites done by your team'),
			action=_('Make Timesheet'),
			route='List/Timesheet',
			domain=('Services',),
			target=5
		),
		dataent._dict(
			doctype='Student',
			title=_('Add Students'),
			description=_('Students are at the heart of the system, add all your students'),
			action=_('Make Student'),
			route='List/Student',
			domain=('Education',),
			target=5
		),
		dataent._dict(
			doctype='Student Batch',
			title=_('Group your students in batches'),
			description=_('Student Batches help you track attendance, assessments and fees for students'),
			action=_('Make Student Batch'),
			route='List/Student Batch',
			domain=('Education',),
			target=3
		),
		dataent._dict(
			doctype='Employee',
			title=_('Create Employee Records'),
			description=_('Create Employee records to manage leaves, expense claims and payroll'),
			action=_('Make Employee'),
			route='List/Employee',
			target=3
		)
	]

	for m in message_settings:
		if not m.domain or domain in m.domain:
			m.count = dataent.db.count(m.doctype)
			if m.count < m.target:
				messages.append(m)

	return messages
