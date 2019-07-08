// Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

dataent.require("assets/epaas/js/financial_statements.js", function() {
	dataent.query_reports["Balance Sheet"] = epaas.financial_statements;

	dataent.query_reports["Balance Sheet"]["filters"].push({
		"fieldname": "accumulated_values",
		"label": __("Accumulated Values"),
		"fieldtype": "Check",
		"default": 1
	});

	dataent.query_reports["Balance Sheet"]["filters"].push({
		"fieldname": "include_default_book_entries",
		"label": __("Include Default Book Entries"),
		"fieldtype": "Check"
	});
});
