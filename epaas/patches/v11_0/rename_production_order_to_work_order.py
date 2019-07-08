# Copyright (c) 2018, Dataent and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
from dataent.model.rename_doc import rename_doc
from dataent.model.utils.rename_field import rename_field
import dataent

def execute():
	rename_doc('DocType', 'Production Order', 'Work Order', force=True)
	dataent.reload_doc('manufacturing', 'doctype', 'work_order')

	rename_doc('DocType', 'Production Order Item', 'Work Order Item', force=True)
	dataent.reload_doc('manufacturing', 'doctype', 'work_order_item')

	rename_doc('DocType', 'Production Order Operation', 'Work Order Operation', force=True)
	dataent.reload_doc('manufacturing', 'doctype', 'work_order_operation')

	dataent.reload_doc('projects', 'doctype', 'timesheet')
	dataent.reload_doc('stock', 'doctype', 'stock_entry')
	rename_field("Timesheet", "production_order", "work_order")
	rename_field("Stock Entry", "production_order", "work_order")

	dataent.rename_doc("Report", "Production Orders in Progress", "Work Orders in Progress", force=True)
	dataent.rename_doc("Report", "Completed Production Orders", "Completed Work Orders", force=True)
	dataent.rename_doc("Report", "Open Production Orders", "Open Work Orders", force=True)
	dataent.rename_doc("Report", "Issued Items Against Production Order", "Issued Items Against Work Order", force=True)
	dataent.rename_doc("Report", "Production Order Stock Report", "Work Order Stock Report", force=True)

	dataent.db.sql("""update `tabDesktop Icon` \
		set label='Work Order', module_name='Work Order' \
		where label='Production Order'""")
	dataent.db.sql("""update `tabDesktop Icon` \
		set link='List/Work Order' \
		where link='List/Production Order'""")
