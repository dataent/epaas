from __future__ import unicode_literals

import dataent
from dataent import _

no_cache = 1
no_sitemap = 1

def get_context(context):
	if dataent.session.user=='Guest':
		dataent.throw(_("You need to be logged in to access this page"), dataent.PermissionError)

	context.show_sidebar=True

	if dataent.db.exists("Patient", {'email': dataent.session.user}):
		patient = dataent.get_doc("Patient", {'email': dataent.session.user})
		context.doc = patient
		dataent.form_dict.new = 0
		dataent.form_dict.name = patient.name

def get_patient():
	return dataent.get_value("Patient",{"email": dataent.session.user}, "name")

def has_website_permission(doc, ptype, user, verbose=False):
	if doc.name == get_patient():
		return True
	else:
		return False
