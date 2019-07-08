// Copyright (c) 2018, Dataent Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

dataent.query_reports["Lead Conversion Time"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			'reqd': 1,
			"default": dataent.datetime.add_days(dataent.datetime.nowdate(), -30)
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			'reqd': 1,
			"default":dataent.datetime.nowdate()
		},
	]
};


