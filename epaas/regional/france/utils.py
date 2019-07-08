# Copyright (c) 2018, Dataent Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import dataent
from dataent import _
from epaas import get_region

def create_transaction_log(doc, method):
	region = get_region()
	if region not in ["France"]:
		return
	else:
		data = str(doc.as_dict())

		dataent.get_doc({
			"doctype": "Transaction Log",
			"reference_doctype": doc.doctype,
			"document_name": doc.name,
			"data": data
		}).insert(ignore_permissions=True)

# don't remove this function it is used in tests
def test_method():
	'''test function'''
	return 'overridden'
