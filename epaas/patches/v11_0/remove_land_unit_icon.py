# Copyright (c) 2018, Dataent and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals

# imports - module imports
import dataent


def execute():
	"""
	Delete the "Land Unit" doc if exists from "Desktop Icon" doctype
	"""
	try:
		doc = dataent.get_doc('Desktop Icon', {'standard': 1, 'module_name': 'Land Unit'})
		dataent.delete_doc('Desktop Icon', doc.name)
	except dataent.ValidationError:
		# The 'Land Unit' doc doesn't exist, nothing to do
		pass
