# -*- coding: utf-8 -*-
# Copyright (c) 2018, Dataent Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import dataent
from dataent import _
from dataent.model.document import Document

class ItemAlternative(Document):
	def validate(self):
		self.has_alternative_item()
		self.validate_alternative_item()
		self.validate_duplicate()

	def has_alternative_item(self):
		if (self.item_code and
			not dataent.db.get_value('Item', self.item_code, 'allow_alternative_item')):
			dataent.throw(_("Not allow to set alternative item for the item {0}").format(self.item_code))

	def validate_alternative_item(self):
		if self.item_code == self.alternative_item_code:
			dataent.throw(_("Alternative item must not be same as item code"))

	def validate_duplicate(self):
		if dataent.db.get_value("Item Alternative", {'item_code': self.item_code,
			'alternative_item_code': self.alternative_item_code, 'name': ('!=', self.name)}):
			dataent.throw(_("Already record exists for the item {0}".format(self.item_code)))

def get_alternative_items(doctype, txt, searchfield, start, page_len, filters):
	return dataent.db.sql(""" (select alternative_item_code from `tabItem Alternative`
			where item_code = %(item_code)s and alternative_item_code like %(txt)s)
		union
			(select item_code from `tabItem Alternative`
			where alternative_item_code = %(item_code)s and item_code like %(txt)s
			and two_way = 1) limit {0}, {1}
		""".format(start, page_len), {
			"item_code": dataent.db.escape(filters.get('item_code')),
			"txt": "%%%s%%" % dataent.db.escape(txt)
		})