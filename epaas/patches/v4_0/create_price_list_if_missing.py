# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent
from dataent import _
from dataent.utils.nestedset import get_root_of

def execute():
	# setup not complete
	if not dataent.db.sql("""select name from tabCompany limit 1"""):
		return

	if "shopping_cart" in dataent.get_installed_apps():
		dataent.reload_doc("shopping_cart", "doctype", "shopping_cart_settings")

	if not dataent.db.sql("select name from `tabPrice List` where buying=1"):
		create_price_list(_("Standard Buying"), buying=1)

	if not dataent.db.sql("select name from `tabPrice List` where selling=1"):
		create_price_list(_("Standard Selling"), selling=1)

def create_price_list(pl_name, buying=0, selling=0):
	price_list = dataent.get_doc({
		"doctype": "Price List",
		"price_list_name": pl_name,
		"enabled": 1,
		"buying": buying,
		"selling": selling,
		"currency": dataent.db.get_default("currency"),
		"territories": [{
			"territory": get_root_of("Territory")
		}]
	})
	price_list.insert()
