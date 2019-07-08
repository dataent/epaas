# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dataent Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import dataent
from dataent.model.document import Document

class Fertilizer(Document):
	def load_contents(self):
		docs = dataent.get_all("Agriculture Analysis Criteria", filters={'linked_doctype':'Fertilizer'})
		for doc in docs:
			self.append('fertilizer_contents', {'title': str(doc.name)})