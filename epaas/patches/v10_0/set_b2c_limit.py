# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doc("regional", "doctype", "gst_settings")
	dataent.reload_doc("accounts", "doctype", "gst_account")
	gst_settings = dataent.get_doc("GST Settings")
	gst_settings.b2c_limit = 250000
	gst_settings.save()
