// Copyright (c) 2016, Dataent Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
dataent.require("assets/epaas/js/financial_statements.js", function() {
	dataent.query_reports["Vehicle Expenses"] = {
		"filters": [
			{
				"fieldname": "fiscal_year",
				"label": __("Fiscal Year"),
				"fieldtype": "Link",
				"options": "Fiscal Year",
				"default": dataent.defaults.get_user_default("fiscal_year"),
				"reqd": 1,
				"on_change": function(query_report) {
					var fiscal_year = query_report.get_values().fiscal_year;
					if (!fiscal_year) {
						return;
					}
					dataent.model.with_doc("Fiscal Year", fiscal_year, function(r) {
						var fy = dataent.model.get_doc("Fiscal Year", fiscal_year);

						dataent.query_report.set_filter({
							from_date: fy.year_start_date,
							to_date: fy.year_end_date
						});
					});
				}
			}
		]
	}
});

