// Copyright (c) 2018, Dataent Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
dataent.views.calendar["Attendance"] = {
	field_map: {
		"start": "attendance_date",
		"end": "attendance_date",
		"id": "name",
		"docstatus": 1
	},
	options: {
		header: {
			left: 'prev,next today',
			center: 'title',
			right: 'month'
		}
	},
	get_events_method: "epaas.hr.doctype.attendance.attendance.get_events"
};