# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent
from dataent import _, throw
from dataent.utils import cint
from dataent.model.document import Document
import dataent.defaults

class PriceList(Document):
	def validate(self):
		if not cint(self.buying) and not cint(self.selling):
			throw(_("Price List must be applicable for Buying or Selling"))

	def on_update(self):
		self.set_default_if_missing()
		self.update_item_price()

	def set_default_if_missing(self):
		if cint(self.selling):
			if not dataent.db.get_value("Selling Settings", None, "selling_price_list"):
				dataent.set_value("Selling Settings", "Selling Settings", "selling_price_list", self.name)

		elif cint(self.buying):
			if not dataent.db.get_value("Buying Settings", None, "buying_price_list"):
				dataent.set_value("Buying Settings", "Buying Settings", "buying_price_list", self.name)

	def update_item_price(self):
		dataent.db.sql("""update `tabItem Price` set currency=%s,
			buying=%s, selling=%s, modified=NOW() where price_list=%s""",
			(self.currency, cint(self.buying), cint(self.selling), self.name))

	def on_trash(self):
		def _update_default_price_list(module):
			b = dataent.get_doc(module + " Settings")
			price_list_fieldname = module.lower() + "_price_list"

			if self.name == b.get(price_list_fieldname):
				b.set(price_list_fieldname, None)
				b.flags.ignore_permissions = True
				b.save()

		for module in ["Selling", "Buying"]:
			_update_default_price_list(module)
