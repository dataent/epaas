from __future__ import unicode_literals
import dataent

def execute():
	for doc in dataent.get_all("Sales Order", filters={"docstatus": 1,
		"order_type": "Maintenance"}):
		doc = dataent.get_doc("Sales Order", doc.name)
		doc.set_status(update=True)
