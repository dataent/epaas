from __future__ import unicode_literals
import dataent

def execute():
	for d in dataent.db.get_all("Stock Entry"):
		se = dataent.get_doc("Stock Entry", d.name)
		se.set_total_incoming_outgoing_value()
		se.db_update()
