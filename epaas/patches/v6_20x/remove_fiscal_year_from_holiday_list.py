from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doctype("Holiday List")

	default_holiday_list = dataent.db.get_value("Holiday List", {"is_default": 1})
	if default_holiday_list:
		for company in dataent.get_all("Company", fields=["name", "default_holiday_list"]):
			if not company.default_holiday_list:
				dataent.db.set_value("Company", company.name, "default_holiday_list", default_holiday_list)


	fiscal_years = dataent._dict((fy.name, fy) for fy in dataent.get_all("Fiscal Year", fields=["name", "year_start_date", "year_end_date"]))

	for holiday_list in dataent.get_all("Holiday List", fields=["name", "fiscal_year"]):
		fy = fiscal_years[holiday_list.fiscal_year]
		dataent.db.set_value("Holiday List", holiday_list.name, "from_date", fy.year_start_date)
		dataent.db.set_value("Holiday List", holiday_list.name, "to_date", fy.year_end_date)
