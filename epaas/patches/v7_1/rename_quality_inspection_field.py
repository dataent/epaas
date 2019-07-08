from __future__ import unicode_literals
import dataent
from dataent.model.utils.rename_field import *

def execute():
	for doctype in ("Purchase Receipt Item", "Delivery Note Item"):
		dataent.reload_doctype(doctype)

		table_columns = dataent.db.get_table_columns(doctype)
		if "qa_no" in table_columns:
			rename_field(doctype, "qa_no", "quality_inspection")

	dataent.reload_doctype("Item")
	rename_field("Item", "inspection_required", "inspection_required_before_purchase")

	dataent.reload_doc('stock', 'doctype', 'quality_inspection')
	dataent.db.sql("""
		update
			`tabQuality Inspection`
		set
			reference_type = 'Purchase Receipt', reference_name = purchase_receipt_no
		where
			ifnull(purchase_receipt_no, '') != '' and inspection_type = 'Incoming'
	""")

	dataent.db.sql("""
		update
			`tabQuality Inspection`
		set
			reference_type = 'Delivery Note', reference_name = delivery_note_no
		where
			ifnull(delivery_note_no, '') != '' and inspection_type = 'Outgoing'
	""")

	for old_fieldname in ["purchase_receipt_no", "delivery_note_no"]:
		update_reports("Quality Inspection", old_fieldname, "reference_name")
		update_users_report_view_settings("Quality Inspection", old_fieldname, "reference_name")
		update_property_setters("Quality Inspection", old_fieldname, "reference_name")
