// Copyright (c) 2013, Dataent Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

dataent.require("assets/epaas/js/financial_statements.js", function() {
	dataent.query_reports["Cash Flow"] = $.extend({},
		epaas.financial_statements);

	// The last item in the array is the definition for Presentation Currency
	// filter. It won't be used in cash flow for now so we pop it. Please take
	// of this if you are working here.
	dataent.query_reports["Cash Flow"]["filters"].pop();

	dataent.query_reports["Cash Flow"]["filters"].push({
		"fieldname": "accumulated_values",
		"label": __("Accumulated Values"),
		"fieldtype": "Check"
	});

	dataent.query_reports["Cash Flow"]["filters"].push({
		"fieldname": "include_default_book_entries",
		"label": __("Include Default Book Entries"),
		"fieldtype": "Check"
	});
});