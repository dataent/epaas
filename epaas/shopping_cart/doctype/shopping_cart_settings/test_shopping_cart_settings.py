# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
import dataent
import unittest
from epaas.shopping_cart.doctype.shopping_cart_settings.shopping_cart_settings import ShoppingCartSetupError

class TestShoppingCartSettings(unittest.TestCase):
	def setUp(self):
		dataent.db.sql("""delete from `tabSingles` where doctype="Shipping Cart Settings" """)

	def get_cart_settings(self):
		return dataent.get_doc({"doctype": "Shopping Cart Settings",
			"company": "_Test Company"})

	def test_exchange_rate_exists(self):
		dataent.db.sql("""delete from `tabCurrency Exchange`""")

		cart_settings = self.get_cart_settings()
		cart_settings.price_list = "_Test Price List Rest of the World"
		self.assertRaises(ShoppingCartSetupError, cart_settings.validate_exchange_rates_exist)

		from epaas.setup.doctype.currency_exchange.test_currency_exchange import test_records as \
			currency_exchange_records
		dataent.get_doc(currency_exchange_records[0]).insert()
		cart_settings.validate_exchange_rates_exist()

	def test_tax_rule_validation(self):
		dataent.db.sql("update `tabTax Rule` set use_for_shopping_cart = 0")
		dataent.db.commit()

		cart_settings = self.get_cart_settings()
		cart_settings.enabled = 1
		if not dataent.db.get_value("Tax Rule", {"use_for_shopping_cart": 1}, "name"):
			self.assertRaises(ShoppingCartSetupError, cart_settings.validate_tax_rule)
			
		dataent.db.sql("update `tabTax Rule` set use_for_shopping_cart = 1")

test_dependencies = ["Tax Rule"]