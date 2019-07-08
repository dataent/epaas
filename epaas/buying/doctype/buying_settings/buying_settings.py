# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
import dataent

from dataent.model.document import Document

class BuyingSettings(Document):
	def validate(self):
		for key in ["supplier_group", "supp_master_name", "maintain_same_rate", "buying_price_list"]:
			dataent.db.set_default(key, self.get(key, ""))

		from epaas.setup.doctype.naming_series.naming_series import set_by_naming_series
		set_by_naming_series("Supplier", "supplier_name",
			self.get("supp_master_name")=="Naming Series", hide_name_field=False)
