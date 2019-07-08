# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

def execute():
	for d in dataent.db.sql("select name from `tabBOM` where docstatus < 2"):
		try:
			document = dataent.get_doc('BOM', d[0])
			if document.docstatus == 1:
				document.flags.ignore_validate_update_after_submit = True
				document.calculate_cost()
			document.save()
		except:
			pass
