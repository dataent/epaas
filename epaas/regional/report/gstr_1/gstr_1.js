// Copyright (c) 2018, Dataent Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

dataent.query_reports["GSTR-1"] = {
	"filters": [
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"reqd": 1,
			"default": dataent.defaults.get_user_default("Company")
		},
		{
			"fieldname":"company_address",
			"label": __("Address"),
			"fieldtype": "Link",
			"options": "Address",
			"get_query": function() {
				var company = dataent.query_report.get_filter_value('company');
				if (company) {
					return {
						"query": 'dataent.contacts.doctype.address.address.address_query',
						"filters": { link_doctype: 'Company', link_name: company}
					};
				}
			}
		},
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"reqd": 1,
			"default": dataent.datetime.add_months(dataent.datetime.get_today(), -3),
			"width": "80"
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"reqd": 1,
			"default": dataent.datetime.get_today()
		},
		{
			"fieldname":"type_of_business",
			"label": __("Type of Business"),
			"fieldtype": "Select",
			"reqd": 1,
			"options": ["B2B", "B2C Large", "B2C Small","CDNR", "EXPORT"],
			"default": "B2B"
		}
	]
}
