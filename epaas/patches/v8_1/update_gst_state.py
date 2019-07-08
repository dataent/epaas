from __future__ import unicode_literals
import dataent
from epaas.regional.india import states

def execute():
	company = dataent.get_all('Company', filters = {'country': 'India'})
	if not company:
		return

	if not dataent.db.get_value("Custom Field", filters={'fieldname':'gst_state'}):
		return

	dataent.db.sql("update `tabCustom Field` set options=%s where fieldname='gst_state'", '\n'.join(states))
	dataent.db.sql("update `tabAddress` set gst_state='Chhattisgarh' where gst_state='Chattisgarh'")
	dataent.db.sql("update `tabAddress` set gst_state_number='05' where gst_state='Uttarakhand'")
