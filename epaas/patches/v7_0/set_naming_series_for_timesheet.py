# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals

import dataent
from dataent.custom.doctype.property_setter.property_setter import make_property_setter

def execute():
	dataent.reload_doc('projects', 'doctype', 'timesheet')
	dataent.reload_doc('projects', 'doctype', 'timesheet_detail')
	dataent.reload_doc('accounts', 'doctype', 'sales_invoice_timesheet')
	
	make_property_setter('Timesheet', "naming_series", "options", 'TS-', "Text")
	make_property_setter('Timesheet', "naming_series", "default", 'TS-', "Text")