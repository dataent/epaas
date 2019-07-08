from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doctype('System Settings')
	companies = dataent.db.sql("""select name, country
		from tabCompany order by creation asc""", as_dict=True)
	if companies:
		dataent.db.set_value('System Settings', 'System Settings', 'setup_complete', 1)

	for company in companies:
		if company.country:
			dataent.db.set_value('System Settings', 'System Settings', 'country', company.country)
			break


