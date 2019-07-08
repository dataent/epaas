// Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt


dataent.query_reports["Absent Student Report"] = {
	"filters": [
		{
			"fieldname":"date",
			"label": __("Date"),
			"fieldtype": "Date",
			"default": dataent.datetime.get_today(),
			"reqd": 1
		}
	]
}
