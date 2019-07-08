// Copyright (c) 2016, Dataent Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

{% include "epaas/regional/report/india_gst_common/india_gst_common.js" %}

dataent.query_reports["HSN-wise-summary of outward supplies"] = {
	"filters": [
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"reqd": 1,
			"default": dataent.defaults.get_user_default("Company"),
			"on_change": fetch_gstins
		},
		{
			"fieldname":"gst_hsn_code",
			"label": __("HSN/SAC"),
			"fieldtype": "Link",
			"options": "GST HSN Code",
			"width": "80"
		},
		{
			"fieldname":"company_gstin",
			"label": __("Company GSTIN"),
			"fieldtype": "Select",
			"placeholder":"Company GSTIN",
			"options": [""],
			"width": "80"
		},
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"width": "80"
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"width": "80"
		},

	],
	onload: (report) => {
		fetch_gstins(report);
	}
};
