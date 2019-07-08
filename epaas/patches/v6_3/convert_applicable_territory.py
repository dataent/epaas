from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doc("stock", "doctype", "price_list_country")
	dataent.reload_doc("accounts", "doctype", "shipping_rule_country")
	dataent.reload_doctype("Price List")
	dataent.reload_doctype("Shipping Rule")
	dataent.reload_doctype("shopping_cart", "doctype", "shopping_cart_settings")

	# for price list
	countries = dataent.db.sql_list("select name from tabCountry")

	for doctype in ("Price List", "Shipping Rule"):
		for at in dataent.db.sql("""select name, parent, territory from `tabApplicable Territory` where
			parenttype = %s """, doctype, as_dict=True):
			if at.territory in countries:
				parent = dataent.get_doc(doctype, at.parent)
				if not parent.countries:
					parent.append("countries", {"country": at.territory})
				parent.save()


	dataent.delete_doc("DocType", "Applicable Territory")
