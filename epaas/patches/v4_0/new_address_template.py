from __future__ import print_function, unicode_literals
import dataent

def execute():
	dataent.reload_doc("utilities", "doctype", "address_template")
	if not dataent.db.sql("select name from `tabAddress Template`"):
		try:
			d = dataent.new_doc("Address Template")
			d.update({"country":dataent.db.get_default("country") or
				dataent.db.get_value("Global Defaults", "Global Defaults", "country")})
			d.insert()
		except:
			print(dataent.get_traceback())

