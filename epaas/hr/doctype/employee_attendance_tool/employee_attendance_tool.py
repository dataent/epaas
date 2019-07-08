# -*- coding: utf-8 -*-
# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import dataent
import json
from dataent.model.document import Document


class EmployeeAttendanceTool(Document):
	pass


@dataent.whitelist()
def get_employees(date, department = None, branch = None, company = None):
	attendance_not_marked = []
	attendance_marked = []
	filters = {"status": "Active", "date_of_joining": ["<=", date]}

	for field, value in {'department': department,
		'branch': branch, 'company': company}.items():
		if value:
			filters[field] = value

	employee_list = dataent.get_list("Employee", fields=["employee", "employee_name"], filters=filters, order_by="employee_name")
	marked_employee = {}
	for emp in dataent.get_list("Attendance", fields=["employee", "status"],
							   filters={"attendance_date": date}):
		marked_employee[emp['employee']] = emp['status']

	for employee in employee_list:
		employee['status'] = marked_employee.get(employee['employee'])
		if employee['employee'] not in marked_employee:
			attendance_not_marked.append(employee)
		else:
			attendance_marked.append(employee)
	return {
		"marked": attendance_marked,
		"unmarked": attendance_not_marked
	}


@dataent.whitelist()
def mark_employee_attendance(employee_list, status, date, leave_type=None, company=None):
	employee_list = json.loads(employee_list)
	for employee in employee_list:
		attendance = dataent.new_doc("Attendance")
		attendance.employee = employee['employee']
		attendance.employee_name = employee['employee_name']
		attendance.attendance_date = date
		attendance.status = status
		if status == "On Leave" and leave_type:
			attendance.leave_type = leave_type
		if company:
			attendance.company = company
		else:
			attendance.company = dataent.db.get_value("Employee", employee['employee'], "Company")
		attendance.submit()
