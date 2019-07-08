# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent
from dataent import _


class ItemPriceDuplicateItem(dataent.ValidationError): pass


from dataent.model.document import Document


class ItemPrice(Document):
	
	def validate(self):
		self.validate_item()
		self.validate_dates()
		self.update_price_list_details()
		self.update_item_details()
		self.check_duplicates()

	def validate_item(self):
		if not dataent.db.exists("Item", self.item_code):
			dataent.throw(_("Item {0} not found").format(self.item_code))

	def validate_dates(self):
		if self.valid_from and self.valid_upto:
			if self.valid_from > self.valid_upto:
				dataent.throw(_("Valid From Date must be lesser than Valid Upto Date."))

	def update_price_list_details(self):
		self.buying, self.selling, self.currency = \
			dataent.db.get_value("Price List",
								{"name": self.price_list, "enabled": 1},
								["buying", "selling", "currency"])

	def update_item_details(self):
		self.item_name, self.item_description = dataent.db.get_value("Item",self.item_code,["item_name", "description"])

	def check_duplicates(self):
		conditions = "where item_code=%(item_code)s and price_list=%(price_list)s and name != %(name)s"

		for field in ['uom', 'min_qty', 'valid_from',
			'valid_upto', 'packing_unit', 'customer', 'supplier']:
			if self.get(field):
				conditions += " and {0} = %({1})s".format(field, field)

		price_list_rate = dataent.db.sql("""
			SELECT price_list_rate
			FROM `tabItem Price`
			  {conditions} """.format(conditions=conditions), self.as_dict())

		if price_list_rate :
			dataent.throw(_("Item Price appears multiple times based on Price List, Supplier/Customer, Currency, Item, UOM, Qty and Dates."), ItemPriceDuplicateItem)

	def before_save(self):
		if self.selling:
			self.reference = self.customer
		if self.buying:
			self.reference = self.supplier
