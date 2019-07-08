from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doc("website", "doctype", "contact_us_settings")
	address = dataent.db.get_value("Contact Us Settings", None, "address")
	if address:
		address = dataent.get_doc("Address", address)
		contact = dataent.get_doc("Contact Us Settings", "Contact Us Settings")
		for f in ("address_title", "address_line1", "address_line2", "city", "state", "country", "pincode"):
			contact.set(f, address.get(f))
		
		contact.save()