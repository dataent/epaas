# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

from dataent.utils import getdate, nowdate
from dataent import _
from dataent.model.document import Document
from epaas.hr.utils import set_employee_name
from dataent.utils import cstr

class Attendance(Document):
	def validate_duplicate_record(self):
		res = dataent.db.sql("""select name from `tabAttendance` where employee = %s and attendance_date = %s
			and name != %s and docstatus = 1""",
			(self.employee, self.attendance_date, self.name))
		if res:
			dataent.throw(_("Attendance for employee {0} is already marked").format(self.employee))

		set_employee_name(self)

	def check_leave_record(self):
		leave_record = dataent.db.sql("""select leave_type, half_day, half_day_date from `tabLeave Application`
			where employee = %s and %s between from_date and to_date and status = 'Approved'
			and docstatus = 1""", (self.employee, self.attendance_date), as_dict=True)
		if leave_record:
			for d in leave_record:
				if d.half_day_date == getdate(self.attendance_date):
					self.status = 'Half Day'
					dataent.msgprint(_("Employee {0} on Half day on {1}").format(self.employee, self.attendance_date))
				else:
					self.status = 'On Leave'
					self.leave_type = d.leave_type
					dataent.msgprint(_("Employee {0} is on Leave on {1}").format(self.employee, self.attendance_date))

		if self.status == "On Leave" and not leave_record:
			dataent.throw(_("No leave record found for employee {0} for {1}").format(self.employee, self.attendance_date))

	def validate_attendance_date(self):
		date_of_joining = dataent.db.get_value("Employee", self.employee, "date_of_joining")

		if getdate(self.attendance_date) > getdate(nowdate()):
			dataent.throw(_("Attendance can not be marked for future dates"))
		elif date_of_joining and getdate(self.attendance_date) < getdate(date_of_joining):
			dataent.throw(_("Attendance date can not be less than employee's joining date"))

	def validate_employee(self):
		emp = dataent.db.sql("select name from `tabEmployee` where name = %s and status = 'Active'",
		 	self.employee)
		if not emp:
			dataent.throw(_("Employee {0} is not active or does not exist").format(self.employee))

	def validate(self):
		from epaas.controllers.status_updater import validate_status
		validate_status(self.status, ["Present", "Absent", "On Leave", "Half Day"])
		self.validate_attendance_date()
		self.validate_duplicate_record()
		self.check_leave_record()

@dataent.whitelist()
def get_events(start, end, filters=None):
	events = []

	employee = dataent.db.get_value("Employee", {"user_id": dataent.session.user})

	if not employee:
		return events

	from dataent.desk.reportview import get_filters_cond
	conditions = get_filters_cond("Attendance", filters, [])
	add_attendance(events, start, end, conditions=conditions)
	return events

def add_attendance(events, start, end, conditions=None):
	query = """select name, attendance_date, status
		from `tabAttendance` where
		attendance_date between %(from_date)s and %(to_date)s
		and docstatus < 2"""
	if conditions:
		query += conditions

	for d in dataent.db.sql(query, {"from_date":start, "to_date":end}, as_dict=True):
		e = {
			"name": d.name,
			"doctype": "Attendance",
			"date": d.attendance_date,
			"title": cstr(d.status),
			"docstatus": d.docstatus
		}
		if e not in events:
			events.append(e)