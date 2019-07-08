# -*- coding: utf-8 -*-
# Copyright (c) 2018, Dataent Technologies Pvt. Ltd. and Contributors
# See license.txt
from __future__ import unicode_literals

import dataent
import unittest
from dataent.utils import nowdate
from datetime import date

class TestAttendanceRequest(unittest.TestCase):
	def setUp(self):
		for doctype in ["Attendance Request", "Attendance"]:
			dataent.db.sql("delete from `tab{doctype}`".format(doctype=doctype))

	def test_attendance_request(self):
		today = nowdate()
		employee = get_employee()
		attendance_request = dataent.new_doc("Attendance Request")
		attendance_request.employee = employee.name
		attendance_request.from_date = date(date.today().year, 1, 1)
		attendance_request.to_date = date(date.today().year, 1, 2)
		attendance_request.reason = "Work From Home"
		attendance_request.company = "_Test Company"
		attendance_request.insert()
		attendance_request.submit()
		attendance = dataent.get_doc('Attendance', {
			'employee': employee.name,
			'attendance_date': date(date.today().year, 1, 1),
			'docstatus': 1
		})
		self.assertEqual(attendance.status, 'Present')
		attendance_request.cancel()
		attendance.reload()
		self.assertEqual(attendance.docstatus, 2)

def get_employee():
	return dataent.get_doc("Employee", "_T-Employee-00001")