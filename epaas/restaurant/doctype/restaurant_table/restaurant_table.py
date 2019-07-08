# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dataent Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import dataent, re
from dataent.model.document import Document
from dataent.model.naming import make_autoname

class RestaurantTable(Document):
	def autoname(self):
		prefix = re.sub('-+', '-', self.restaurant.replace(' ', '-'))
		self.name = make_autoname(prefix + '-.##')
