# Copyright (c) 2017, Dataent and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent
from dataent.utils import cint

def execute():
	"""
		save system settings document
	"""

	dataent.reload_doc("core", "doctype", "system_settings")
	doc = dataent.get_doc("System Settings")
	doc.flags.ignore_mandatory = True

	if cint(doc.currency_precision) == 0:
		doc.currency_precision = ''

	doc.save(ignore_permissions=True)
