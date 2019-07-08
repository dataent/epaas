from __future__ import unicode_literals
import os

import dataent
from dataent import _


def execute():
	dataent.reload_doc("email", "doctype", "email_template")
	dataent.reload_doc("stock", "doctype", "delivery_settings")

	if not dataent.db.exists("Email Template", _("Dispatch Notification")):
		base_path = dataent.get_app_path("epaas", "stock", "doctype")
		response = dataent.read_file(os.path.join(base_path, "delivery_trip/dispatch_notification_template.html"))

		dataent.get_doc({
			"doctype": "Email Template",
			"name": _("Dispatch Notification"),
			"response": response,
			"subject": _("Your order is out for delivery!"),
			"owner": dataent.session.user,
		}).insert(ignore_permissions=True)

	delivery_settings = dataent.get_doc("Delivery Settings")
	delivery_settings.dispatch_template = _("Dispatch Notification")
	delivery_settings.save()
