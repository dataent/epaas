# Copyright (c) 2018, Dataent and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
from dataent.model.rename_doc import rename_doc
import dataent

def execute():
	rename_doc('DocType', 'Health Insurance', 'Employee Health Insurance', force=True)
	dataent.reload_doc('hr', 'doctype', 'employee_health_insurance')