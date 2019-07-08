// Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

dataent.views.calendar["Training Event"] = {
	field_map: {
		"start": "start_time",
		"end": "end_time",
		"id": "name",
		"title": "event_name",
		"allDay": "allDay"
	},
	gantt: true,
	get_events_method: "dataent.desk.calendar.get_events",
}
