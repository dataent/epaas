// Copyright (c) 2016, Dataent Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

dataent.query_reports["Gross and Net Profit Report"] = {
	"filters": [

	]
}
dataent.require("assets/epaas/js/financial_statements.js", function() {
	dataent.query_reports["Gross and Net Profit Report"] = $.extend({},
		epaas.financial_statements);

	dataent.query_reports["Gross and Net Profit Report"]["filters"].push(
		{
			"fieldname":"project",
			"label": __("Project"),
			"fieldtype": "MultiSelect",
			get_data: function() {
				var projects = dataent.query_report.get_filter_value("project") || "";

				const values = projects.split(/\s*,\s*/).filter(d => d);
				const txt = projects.match(/[^,\s*]*$/)[0] || '';
				let data = [];

				dataent.call({
					type: "GET",
					method:'dataent.desk.search.search_link',
					async: false,
					no_spinner: true,
					args: {
						doctype: "Project",
						txt: txt,
						filters: {
							"name": ["not in", values]
						}
					},
					callback: function(r) {
						data = r.results;
					}
				});
				return data;
			}
		},
		{
			"fieldname": "accumulated_values",
			"label": __("Accumulated Values"),
			"fieldtype": "Check"
		}
	);
});
