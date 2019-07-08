# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

def execute():
	""" 
		disable the instructor role for companies with domain other than
		Education.
	"""

	domains = dataent.db.sql_list("select domain from tabCompany")
	if "Education" not in domains:
		if dataent.db.exists("Role", "Instructor"):
			role = dataent.get_doc("Role", "Instructor")
			role.disabled = 1
			role.save(ignore_permissions=True)