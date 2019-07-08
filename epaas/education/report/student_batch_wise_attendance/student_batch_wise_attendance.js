// Copyright (c) 2016, Dataent Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

dataent.query_reports["Student Batch-Wise Attendance"] = {
	"filters": [{
		"fieldname": "date",
		"label": __("Date"),
		"fieldtype": "Date",
		"default": dataent.datetime.get_today(),
		"reqd": 1
	}]
}