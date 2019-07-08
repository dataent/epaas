# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dataent Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from dataent.model.document import Document
from dataent.contacts.address_and_contact import load_address_and_contact

class Volunteer(Document):
	def onload(self):
		"""Load address and contacts in `__onload`"""
		load_address_and_contact(self)
