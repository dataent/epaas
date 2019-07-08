# Copyright (c) 2013, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

def execute():
	dataent.db.set_value("SMS Settings", "SMS Settings", "sms_sender_name",
		dataent.db.get_single_value("Global Defaults", "sms_sender_name"))
