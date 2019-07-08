# Copyright (c) 2017, Dataent and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
from epaas.regional.italy.setup import make_custom_fields, setup_report
from epaas.regional.italy import state_codes
import dataent

def execute():
	company = dataent.get_all('Company', filters = {'country': 'Italy'})
	if not company:
		return

	dataent.reload_doc('regional', 'report', 'electronic_invoice_register')
	make_custom_fields()
	setup_report()

	# Set state codes
	condition = ""
	for state, code in state_codes.items():
		condition += " when '{0}' then '{1}'".format(dataent.db.escape(state), dataent.db.escape(code))

	if condition:
		condition = "state_code = (case state {0} end),".format(condition)

	dataent.db.sql("""
		UPDATE tabAddress set {condition} country_code = UPPER(ifnull((select code
			from `tabCountry` where name = `tabAddress`.country), ''))
			where country_code is null and state_code is null
	""".format(condition=condition))

	dataent.db.sql("""
		UPDATE `tabSales Invoice Item` si, `tabSales Order` so
			set si.customer_po_no = so.po_no, si.customer_po_date = so.po_date
		WHERE
			si.sales_order = so.name and so.po_no is not null
	""")
