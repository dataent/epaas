# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dataent Technologies Pvt. Ltd. and Contributors
# See license.txt
from __future__ import unicode_literals

import unittest

import epaas
import dataent
from epaas.stock.doctype.delivery_trip.delivery_trip import get_contact_and_address, notify_customers
from epaas.tests.utils import create_test_contact_and_address
from dataent.utils import add_days, flt, now_datetime, nowdate


class TestDeliveryTrip(unittest.TestCase):
	def setUp(self):
		create_driver()
		create_vehicle()
		create_delivery_notification()
		create_test_contact_and_address()

		settings = dataent.get_single("Google Maps Settings")
		settings.home_address = dataent.get_last_doc("Address").name
		settings.save()

		self.delivery_trip = create_delivery_trip()

	def tearDown(self):
		dataent.db.sql("delete from `tabDriver`")
		dataent.db.sql("delete from `tabVehicle`")
		dataent.db.sql("delete from `tabEmail Template`")
		dataent.db.sql("delete from `tabDelivery Trip`")

	def test_delivery_trip_notify_customers(self):
		notify_customers(delivery_trip=self.delivery_trip.name)
		self.delivery_trip.load_from_db()
		self.assertEqual(self.delivery_trip.email_notification_sent, 1)

	def test_unoptimized_route_list_without_locks(self):
		route_list = self.delivery_trip.form_route_list(optimize=False)

		# Return a single list of destinations, from home address and back
		self.assertEqual(len(route_list), 1)
		self.assertEqual(len(route_list[0]), 4)

	def test_unoptimized_route_list_with_locks(self):
		self.delivery_trip.delivery_stops[0].lock = 1
		self.delivery_trip.save()
		route_list = self.delivery_trip.form_route_list(optimize=False)

		# Return a single list of destinations, from home address and back,
		# since the stops don't need to optimized and simple time
		# estimation is enough
		self.assertEqual(len(route_list), 1)
		self.assertEqual(len(route_list[0]), 4)

	def test_optimized_route_list_without_locks(self):
		route_list = self.delivery_trip.form_route_list(optimize=True)

		# Return a single list of destinations, from home address and back,
		# since the route doesn't have any locks to be optimized against
		self.assertEqual(len(route_list), 1)
		self.assertEqual(len(route_list[0]), 4)

	def test_optimized_route_list_with_locks(self):
		self.delivery_trip.delivery_stops[0].lock = 1
		self.delivery_trip.save()
		route_list = self.delivery_trip.form_route_list(optimize=True)

		# Return multiple route lists, taking the home address as start and end
		self.assertEqual(len(route_list), 2)
		self.assertEqual(len(route_list[0]), 2)  # [home_address, locked_stop]
		self.assertEqual(len(route_list[1]), 3)  # [locked_stop, second_stop, home_address]

	def test_delivery_trip_status_draft(self):
		self.assertEqual(self.delivery_trip.status, "Draft")

	def test_delivery_trip_status_scheduled(self):
		self.delivery_trip.submit()
		self.assertEqual(self.delivery_trip.status, "Scheduled")

	def test_delivery_trip_status_cancelled(self):
		self.delivery_trip.submit()
		self.delivery_trip.cancel()
		self.assertEqual(self.delivery_trip.status, "Cancelled")

	def test_delivery_trip_status_in_transit(self):
		self.delivery_trip.submit()
		self.delivery_trip.delivery_stops[0].visited = 1
		self.delivery_trip.save()
		self.assertEqual(self.delivery_trip.status, "In Transit")

	def test_delivery_trip_status_completed(self):
		self.delivery_trip.submit()

		for stop in self.delivery_trip.delivery_stops:
			stop.visited = 1

		self.delivery_trip.save()
		self.assertEqual(self.delivery_trip.status, "Completed")


def create_driver():
	if not dataent.db.exists("Driver", "Newton Scmander"):
		driver = dataent.get_doc({
			"doctype": "Driver",
			"full_name": "Newton Scmander",
			"cell_number": "98343424242",
			"license_number": "B809"
		})
		driver.insert()


def create_delivery_notification():
	if not dataent.db.exists("Email Template", "Delivery Notification"):
		dispatch_template = dataent.get_doc({
			'doctype': 'Email Template',
			'name': 'Delivery Notification',
			'response': 'Test Delivery Trip',
			'subject': 'Test Subject',
			'owner': dataent.session.user
		})
		dispatch_template.insert()

	delivery_settings = dataent.get_single("Delivery Settings")
	delivery_settings.dispatch_template = 'Delivery Notification'
	delivery_settings.save()


def create_vehicle():
	if not dataent.db.exists("Vehicle", "JB 007"):
		vehicle = dataent.get_doc({
			"doctype": "Vehicle",
			"license_plate": "JB 007",
			"make": "Maruti",
			"model": "PCM",
			"last_odometer": 5000,
			"acquisition_date": nowdate(),
			"location": "Mumbai",
			"chassis_no": "1234ABCD",
			"uom": "Litre",
			"vehicle_value": flt(500000)
		})
		vehicle.insert()


def create_delivery_trip(contact=None):
	if not contact:
		contact = get_contact_and_address("_Test Customer")

	delivery_trip = dataent.new_doc("Delivery Trip")
	delivery_trip.update({
		"doctype": "Delivery Trip",
		"company": epaas.get_default_company(),
		"departure_time": add_days(now_datetime(), 5),
		"driver": dataent.db.get_value('Driver', {"full_name": "Newton Scmander"}),
		"vehicle": "JB 007",
		"delivery_stops": [{
			"customer": "_Test Customer",
			"address": contact.shipping_address.parent,
			"contact": contact.contact_person.parent
		},
		{
			"customer": "_Test Customer",
			"address": contact.shipping_address.parent,
			"contact": contact.contact_person.parent
		}]
	})
	delivery_trip.insert()

	return delivery_trip
