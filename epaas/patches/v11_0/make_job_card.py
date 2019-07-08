# Copyright (c) 2017, Dataent and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent
from epaas.manufacturing.doctype.work_order.work_order import create_job_card

def execute():
	dataent.reload_doc('manufacturing', 'doctype', 'work_order')
	dataent.reload_doc('manufacturing', 'doctype', 'work_order_item')
	dataent.reload_doc('manufacturing', 'doctype', 'job_card')
	dataent.reload_doc('manufacturing', 'doctype', 'job_card_item')

	fieldname = dataent.db.get_value('DocField', {'fieldname': 'work_order', 'parent': 'Timesheet'}, 'fieldname')
	if not fieldname:
		fieldname = dataent.db.get_value('DocField', {'fieldname': 'production_order', 'parent': 'Timesheet'}, 'fieldname')
		if not fieldname: return

	for d in dataent.get_all('Timesheet',
		filters={fieldname: ['!=', ""], 'docstatus': 0},
		fields=[fieldname, 'name']):
		if d[fieldname]:
			doc = dataent.get_doc('Work Order', d[fieldname])
			for row in doc.operations:
				create_job_card(doc, row, auto_create=True)
			dataent.delete_doc('Timesheet', d.name)
