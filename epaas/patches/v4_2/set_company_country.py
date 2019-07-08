# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import print_function, unicode_literals
import dataent

def execute():
	country = dataent.db.get_single_value("Global Defaults", "country")
	if not country:
		print("Country not specified in Global Defaults")
		return

	for company in dataent.db.sql_list("""select name from `tabCompany`
		where ifnull(country, '')=''"""):
		dataent.db.set_value("Company", company, "country", country)
