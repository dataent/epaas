from __future__ import unicode_literals

import dataent

def get_context(context):
	context.read_only = 1

def get_list_context(context):
	context.row_template = "epaas/templates/includes/healthcare/appointment_row_template.html"
	context.get_list = get_appointment_list

def get_appointment_list(doctype, txt, filters, limit_start, limit_page_length = 20, order_by='modified desc'):
	patient = get_patient()
	lab_tests = dataent.db.sql("""select * from `tabPatient Appointment`
		where patient = %s and (status = 'Open' or status = 'Scheduled') order by appointment_date""", patient, as_dict = True)
	return lab_tests

def get_patient():
	return dataent.get_value("Patient",{"email": dataent.session.user}, "name")

def has_website_permission(doc, ptype, user, verbose=False):
	if doc.patient == get_patient():
		return True
	else:
		return False