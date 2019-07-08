// Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt


dataent.require("assets/epaas/js/financial_statements.js", function() {
	dataent.query_reports["Profit and Loss Statement"] = $.extend({},
		epaas.financial_statements);

	dataent.query_reports["Profit and Loss Statement"]["filters"].push(
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
		},
		{
			"fieldname": "include_default_book_entries",
			"label": __("Include Default Book Entries"),
			"fieldtype": "Check"
		}
	);
});
