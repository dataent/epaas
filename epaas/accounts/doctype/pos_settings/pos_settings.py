# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dataent Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import dataent
from dataent.model.document import Document

class POSSettings(Document):
	def validate(self):
		self.set_link_for_pos()

	def set_link_for_pos(self):
		link = 'pos' if self.use_pos_in_offline_mode else 'point-of-sale'
		dataent.db.sql(""" update `tabDesktop Icon` set link = '{0}'
			where module_name like '%pos%'""".format(link))