# -*- coding: utf-8 -*-
# Copyright (c) 2018, Dataent Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import dataent
from dataent import _
from dataent.model.document import Document
from dataent.utils import cint, cstr, date_diff, flt, formatdate, getdate

class OverlapError(dataent.ValidationError): pass

class ShiftAssignment(Document):
	def validate(self):
		self.validate_overlapping_dates()

	def validate_overlapping_dates(self):
			if not self.name:
				self.name = "New Shift Assignment"

			d = dataent.db.sql("""
				select
					name, shift_type, date
				from `tabShift Assignment`
				where employee = %(employee)s and docstatus < 2
				and date = %(date)s
				and name != %(name)s""", {
					"employee": self.employee,
					"shift_type": self.shift_type,
					"date": self.date,
					"name": self.name
				}, as_dict = 1)

			for date_overlap in d:
				if date_overlap['name']:
					self.throw_overlap_error(date_overlap)

	def throw_overlap_error(self, d):
		msg = _("Employee {0} has already applied for {1} on {2} : ").format(self.employee,
			d['shift_type'], formatdate(d['date'])) \
			+ """ <b><a href="#Form/Shift Assignment/{0}">{0}</a></b>""".format(d["name"])
		dataent.throw(msg, OverlapError)

@dataent.whitelist()
def get_events(start, end, filters=None):
	events = []

	employee = dataent.db.get_value("Employee", {"user_id": dataent.session.user}, ["name", "company"],
		as_dict=True)
	if employee:
		employee, company = employee.name, employee.company
	else:
		employee=''
		company=dataent.db.get_value("Global Defaults", None, "default_company")

	from dataent.desk.reportview import get_filters_cond
	conditions = get_filters_cond("Shift Assignment", filters, [])
	add_assignments(events, start, end, conditions=conditions)
	return events

def add_assignments(events, start, end, conditions=None):
	query = """select name, date, employee_name, 
		employee, docstatus
		from `tabShift Assignment` where
		date <= %(date)s
		and docstatus < 2"""
	if conditions:
		query += conditions

	for d in dataent.db.sql(query, {"date":start, "date":end}, as_dict=True):
		e = {
			"name": d.name,
			"doctype": "Shift Assignment",
			"date": d.date,
			"title": cstr(d.employee_name) + \
				cstr(d.shift_type),
			"docstatus": d.docstatus
		}
		if e not in events:
			events.append(e)
