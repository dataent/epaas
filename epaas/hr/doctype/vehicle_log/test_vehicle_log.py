# -*- coding: utf-8 -*-
# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# See license.txt
from __future__ import unicode_literals

import dataent
import unittest
from dataent.utils import nowdate,flt, cstr,random_string
# test_records = dataent.get_test_records('Vehicle Log')
class TestVehicleLog(unittest.TestCase):
	def test_make_vehicle_log(self):
		license_plate=random_string(10).upper()
		employee_id=dataent.db.sql("""select name from `tabEmployee` order by modified desc limit 1""")[0][0]
		vehicle = dataent.get_doc({
			"doctype": "Vehicle",
			"license_plate": cstr(license_plate),
			"make": "Maruti",
			"model": "PCM",
			"last_odometer":5000,
			"acquisition_date":dataent.utils.nowdate(),
			"location": "Mumbai",
			"chassis_no": "1234ABCD",
			"uom": "Litre",
			"vehicle_value":dataent.utils.flt(500000)
		})
		try:
			vehicle.insert()
		except dataent.DuplicateEntryError:
			pass
		vehicle_log = dataent.get_doc({
			"doctype": "Vehicle Log",
			"license_plate": cstr(license_plate),
			"employee":employee_id,
			"date":dataent.utils.nowdate(),
			"odometer":5010,
			"fuel_qty":dataent.utils.flt(50),
			"price": dataent.utils.flt(500)
		})
		vehicle_log.insert()
		vehicle_log.submit()