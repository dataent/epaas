# Copyright (c) 2013, Dataent Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import dataent
from dataent import _
from dataent.utils import add_days, date_diff

from epaas.hotels.doctype.hotel_room_reservation.hotel_room_reservation import get_rooms_booked

def execute(filters=None):
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data

def get_columns(filters):
	columns = [
		dict(label=_("Room Type"), fieldname="room_type"),
		dict(label=_("Rooms Booked"), fieldtype="Int")
	]
	return columns

def get_data(filters):
	out = []
	for room_type in dataent.get_all('Hotel Room Type'):
		total_booked = 0
		for i in range(date_diff(filters.to_date, filters.from_date)):
			day = add_days(filters.from_date, i)
			total_booked += get_rooms_booked(room_type.name, day)

		out.append([room_type.name, total_booked])

	return out