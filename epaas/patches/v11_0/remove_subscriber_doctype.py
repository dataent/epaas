from __future__ import unicode_literals
import dataent
from dataent.model.utils.rename_field import rename_field

def execute():
	""" copy subscribe field to customer """
	dataent.reload_doc("accounts","doctype","subscription")

	if dataent.db.exists("DocType", "Subscriber"):
		if dataent.db.has_column('Subscription','subscriber'):
			dataent.db.sql("""
				update `tabSubscription` s1
				set customer=(select customer from tabSubscriber where name=s1.subscriber)
			""")

		dataent.delete_doc("DocType", "Subscriber")