# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


from __future__ import unicode_literals
import unittest
import dataent
import dataent.defaults

class TestPurchaseOrder(unittest.TestCase):
	def test_make_purchase_order(self):
		from epaas.buying.doctype.supplier_quotation.supplier_quotation import make_purchase_order

		sq = dataent.copy_doc(test_records[0]).insert()

		self.assertRaises(dataent.ValidationError, make_purchase_order,
			sq.name)

		sq = dataent.get_doc("Supplier Quotation", sq.name)
		sq.submit()
		po = make_purchase_order(sq.name)

		self.assertEqual(po.doctype, "Purchase Order")
		self.assertEqual(len(po.get("items")), len(sq.get("items")))

		po.naming_series = "_T-Purchase Order-"

		for doc in po.get("items"):
			if doc.get("item_code"):
				doc.set("schedule_date", "2013-04-12")

		po.insert()

test_records = dataent.get_test_records('Supplier Quotation')
