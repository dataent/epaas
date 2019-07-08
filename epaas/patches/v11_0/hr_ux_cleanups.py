from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doctype('Employee')
	dataent.db.sql('update tabEmployee set first_name = employee_name')

	# update holiday list
	dataent.reload_doctype('Holiday List')
	for holiday_list in dataent.get_all('Holiday List'):
		holiday_list = dataent.get_doc('Holiday List', holiday_list.name)
		holiday_list.db_set('total_holidays', len(holiday_list.holidays), update_modified = False)

