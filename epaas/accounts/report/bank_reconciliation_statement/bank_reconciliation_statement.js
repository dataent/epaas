// Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

dataent.query_reports["Bank Reconciliation Statement"] = {
	"filters": [
		{
			"fieldname":"account",
			"label": __("Bank Account"),
			"fieldtype": "Link",
			"options": "Account",
			"default": dataent.defaults.get_user_default("Company")? 
				locals[":Company"][dataent.defaults.get_user_default("Company")]["default_bank_account"]: "",
			"reqd": 1,
			"get_query": function() {
				return {
					"query": "epaas.controllers.queries.get_account_list",
					"filters": [
						['Account', 'account_type', 'in', 'Bank, Cash'],
						['Account', 'is_group', '=', 0],
					]
				}
			}
		},
		{
			"fieldname":"report_date",
			"label": __("Date"),
			"fieldtype": "Date",
			"default": dataent.datetime.get_today(),
			"reqd": 1
		},
		{
			"fieldname":"include_pos_transactions",
			"label": __("Include POS Transactions"),
			"fieldtype": "Check"
		},
	]
}