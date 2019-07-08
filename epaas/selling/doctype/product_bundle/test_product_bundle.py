
# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt
from __future__ import unicode_literals


import dataent
test_records = dataent.get_test_records('Product Bundle')

def make_product_bundle(parent, items):
	if dataent.db.exists("Product Bundle", parent):
		return dataent.get_doc("Product Bundle", parent)

	product_bundle = dataent.get_doc({
		"doctype": "Product Bundle",
		"new_item_code": parent
	})

	for item in items:
		product_bundle.append("items", {"item_code": item, "qty": 1})

	product_bundle.insert()

	return product_bundle
