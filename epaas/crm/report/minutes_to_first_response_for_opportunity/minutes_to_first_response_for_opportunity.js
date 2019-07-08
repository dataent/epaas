// Copyright (c) 2016, Dataent Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

dataent.query_reports["Minutes to First Response for Opportunity"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			'reqd': 1,
			"default": dataent.datetime.add_days(dataent.datetime.nowdate(), -30)
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			'reqd': 1,
			"default": dataent.datetime.nowdate()
		},
	],
	get_chart_data: function (columns, result) {
		return {
			data: {
				labels: result.map(d => d[0]),
				datasets: [{
					name: 'Mins to first response',
					values: result.map(d => d[1])
				}]
			},
			type: 'line',
		}
	}
}
