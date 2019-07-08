# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dataent Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import dataent
from dataent.model.document import Document

class HotelRoom(Document):
	def validate(self):
		if not self.capacity:
			self.capacity, self.extra_bed_capacity = dataent.db.get_value('Hotel Room Type',
					self.hotel_room_type, ['capacity', 'extra_bed_capacity'])