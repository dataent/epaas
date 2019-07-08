from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doctype("Leave Allocation")
	if dataent.db.has_column("Leave Allocation", "fiscal_year"):
		for leave_allocation in dataent.db.sql("select name, fiscal_year from `tabLeave Allocation`", as_dict=True):
			dates = dataent.db.get_value("Fiscal Year", leave_allocation["fiscal_year"],
				["year_start_date", "year_end_date"])

			if dates:
				year_start_date, year_end_date = dates

				dataent.db.sql("""update `tabLeave Allocation`
					set from_date=%s, to_date=%s where name=%s""",
					(year_start_date, year_end_date, leave_allocation["name"]))

