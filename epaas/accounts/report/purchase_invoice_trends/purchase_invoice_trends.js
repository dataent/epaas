// Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

dataent.require("assets/epaas/js/purchase_trends_filters.js", function() {
	dataent.query_reports["Purchase Invoice Trends"] = {
		filters: epaas.get_purchase_trends_filters()
	}
});