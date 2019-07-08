# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
import dataent

from dataent.model.document import Document

class HRSettings(Document):
	def validate(self):
		from epaas.setup.doctype.naming_series.naming_series import set_by_naming_series
		set_by_naming_series("Employee", "employee_number",
			self.get("emp_created_by")=="Naming Series", hide_name_field=True)
