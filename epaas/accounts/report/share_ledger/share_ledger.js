// -*- coding: utf-8 -*-
// Copyright (c) 2017, Dataent Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

dataent.query_reports["Share Ledger"] = {
	"filters": [
		{
			"fieldname":"date",
			"label": __("Date"),
			"fieldtype": "Date",
			"default": dataent.datetime.get_today(),
			"reqd": 1
		},
		{
			"fieldname":"shareholder",
			"label": __("Shareholder"),
			"fieldtype": "Link",
			"options": "Shareholder"
		}
	]
};
