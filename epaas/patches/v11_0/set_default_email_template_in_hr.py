from __future__ import unicode_literals
import dataent

def execute():

	hr_settings = dataent.get_single("HR Settings")
	hr_settings.leave_approval_notification_template = "Leave Approval Notification"
	hr_settings.leave_status_notification_template = "Leave Status Notification"
	hr_settings.save()