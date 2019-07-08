from __future__ import unicode_literals
import dataent, os
from dataent import _

def execute():
	dataent.reload_doc("email", "doctype", "email_template")

	if not dataent.db.exists("Email Template", _('Leave Approval Notification')):
		base_path = dataent.get_app_path("epaas", "hr", "doctype")
		response = dataent.read_file(os.path.join(base_path, "leave_application/leave_application_email_template.html"))
		dataent.get_doc({
			'doctype': 'Email Template',
			'name': _("Leave Approval Notification"),
			'response': response,
			'subject': _("Leave Approval Notification"),
			'owner': dataent.session.user,
		}).insert(ignore_permissions=True)


	if not dataent.db.exists("Email Template", _('Leave Status Notification')):
		base_path = dataent.get_app_path("epaas", "hr", "doctype")
		response = dataent.read_file(os.path.join(base_path, "leave_application/leave_application_email_template.html"))
		dataent.get_doc({
			'doctype': 'Email Template',
			'name': _("Leave Status Notification"),
			'response': response,
			'subject': _("Leave Status Notification"),
			'owner': dataent.session.user,
		}).insert(ignore_permissions=True)

