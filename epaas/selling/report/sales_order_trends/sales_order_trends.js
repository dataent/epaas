// Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

dataent.require("assets/epaas/js/sales_trends_filters.js", function() {
	dataent.query_reports["Sales Order Trends"] = {
		filters: epaas.get_sales_trends_filters()
	}
});