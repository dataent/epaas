dataent.query_reports["DATEV"] = {
	"filters": [
		{
			"fieldname": "company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": dataent.defaults.get_user_default("Company") || dataent.defaults.get_global_default("Company"),
			"reqd": 1
		},
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"default": dataent.datetime.month_start(),
			"fieldtype": "Date",
			"reqd": 1
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"default": dataent.datetime.now_date(),
			"fieldtype": "Date",
			"reqd": 1
		}
	],
	onload: function(query_report) {
		query_report.page.add_inner_button("Download DATEV Export", () => {
			const filters = JSON.stringify(query_report.get_values());
			window.open(`/api/method/epaas.regional.report.datev.datev.download_datev_csv?filters=${filters}`);
		});
	}
};
