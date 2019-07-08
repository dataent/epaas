from __future__ import unicode_literals
import dataent, json

def execute():
	from epaas.setup.setup_wizard.operations.install_fixtures import add_uom_data

	dataent.reload_doc("setup", "doctype", "UOM Conversion Factor")
	dataent.reload_doc("setup", "doctype", "UOM")
	dataent.reload_doc("stock", "doctype", "UOM Category")

	if not dataent.db.a_row_exists("UOM Conversion Factor"):
		add_uom_data()
	else:
		# delete conversion data and insert again
		dataent.db.sql("delete from `tabUOM Conversion Factor`")
		try:
			dataent.delete_doc('UOM', 'Hundredweight')
			dataent.delete_doc('UOM', 'Pound Cubic Yard')
		except dataent.LinkExistsError:
			pass

		add_uom_data()
