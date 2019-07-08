# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors and Contributors
# See license.txt

from __future__ import unicode_literals
import dataent
import unittest
from dataent.utils import nowdate
from epaas.stock.doctype.item.test_item import create_item
from epaas.stock.doctype.delivery_note.test_delivery_note import create_delivery_note
from epaas.controllers.stock_controller import QualityInspectionRejectedError, QualityInspectionRequiredError, QualityInspectionNotSubmittedError

# test_records = dataent.get_test_records('Quality Inspection')

class TestQualityInspection(unittest.TestCase):
	def setUp(self):
		create_item("_Test Item with QA")
		dataent.db.set_value("Item", "_Test Item with QA", "inspection_required_before_delivery", 1)

	def test_qa_for_delivery(self):
		dn = create_delivery_note(item_code="_Test Item with QA", do_not_submit=True)
		self.assertRaises(QualityInspectionRequiredError, dn.submit)

		qa = create_quality_inspection(reference_type="Delivery Note", reference_name=dn.name, status="Rejected", submit=True)
		dn.reload()
		self.assertRaises(QualityInspectionRejectedError, dn.submit)

		dataent.db.set_value("Quality Inspection Reading", {"parent": qa.name}, "status", "Accepted")
		dn.reload()
		dn.submit()

	def test_qa_not_submit(self):
		dn = create_delivery_note(item_code="_Test Item with QA", do_not_submit=True)
		qa = create_quality_inspection(reference_type="Delivery Note", reference_name=dn.name, submit = False)
		dn.items[0].quality_inspection = qa.name
		self.assertRaises(QualityInspectionNotSubmittedError, dn.submit)

def create_quality_inspection(**args):
	args = dataent._dict(args)
	qa = dataent.new_doc("Quality Inspection")
	qa.report_date = nowdate()
	qa.inspection_type = args.inspection_type or "Outgoing"
	qa.reference_type = args.reference_type
	qa.reference_name = args.reference_name
	qa.item_code = args.item_code or "_Test Item with QA"
	qa.sample_size = 1
	qa.inspected_by = dataent.session.user
	qa.append("readings", {
		"specification": "Size",
		"status": args.status
	})
	qa.save()
	if args.submit:
		qa.submit()

	return qa
