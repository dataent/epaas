from __future__ import unicode_literals
import dataent

def execute():
	for doctype in ("Sales Order", "Purchase Order"):
		for doc in dataent.get_all(doctype, filters={"docstatus": 1}):
			doc = dataent.get_doc(doctype, doc.name)
			doc.set_status(update=True)
