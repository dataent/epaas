// Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

dataent.query_reports["Item-wise Purchase Register"] = {
	"filters": [
		{
			"fieldname":"date_range",
			"label": __("Date Range"),
			"fieldtype": "DateRange",
			"default": [dataent.datetime.add_months(dataent.datetime.get_today(),-1), dataent.datetime.get_today()],
			"reqd": 1
		},
		{
			"fieldname": "item_code",
			"label": __("Item"),
			"fieldtype": "Link",
			"options": "Item",
		},
		{
			"fieldname":"supplier",
			"label": __("Supplier"),
			"fieldtype": "Link",
			"options": "Supplier"
		},
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": dataent.defaults.get_user_default("Company")
		},
		{
			"fieldname":"mode_of_payment",
			"label": __("Mode of Payment"),
			"fieldtype": "Link",
			"options": "Mode of Payment"
		}
	]
}
