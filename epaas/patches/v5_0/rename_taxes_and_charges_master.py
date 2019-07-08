from __future__ import unicode_literals
import dataent


def execute():
	if dataent.db.table_exists("Sales Taxes and Charges Master"):
		dataent.rename_doc("DocType", "Sales Taxes and Charges Master",
			"Sales Taxes and Charges Template")
		dataent.delete_doc("DocType", "Sales Taxes and Charges Master")

	if dataent.db.table_exists("Purchase Taxes and Charges Master"):
		dataent.rename_doc("DocType", "Purchase Taxes and Charges Master",
			"Purchase Taxes and Charges Template")
		dataent.delete_doc("DocType", "Purchase Taxes and Charges Master")
