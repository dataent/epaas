# -*- coding: utf-8 -*-
# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import dataent
from dataent.utils import cint
from dataent.model.document import Document

class ProductsSettings(Document):
	def validate(self):
		if self.home_page_is_products:
			website_settings = dataent.get_doc('Website Settings')
			website_settings.home_page = 'products'
			website_settings.save()

def home_page_is_products(doc, method):
	'''Called on saving Website Settings'''
	home_page_is_products = cint(dataent.db.get_single_value('Products Settings', 'home_page_is_products'))
	if home_page_is_products:
		doc.home_page = 'products'

