# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dataent Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import dataent
from dataent.model.document import Document

class HotelRoomPackage(Document):
	def validate(self):
		if not self.item:
			item = dataent.get_doc(dict(
				doctype = 'Item',
				item_code = self.name,
				item_group = 'Products',
				is_stock_item = 0,
				stock_uom = 'Unit'
			))
			item.insert()
			self.item = item.name
