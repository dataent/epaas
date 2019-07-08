// Copyright (c) 2018, Dataent Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

dataent.views.calendar["Shift Assignment"] = {
	field_map: {
		"start": "date",
		"end": "date",
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
	get_events_method: "epaas.hr.doctype.shift_assignment.shift_assignment.get_events"
}