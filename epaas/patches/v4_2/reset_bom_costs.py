# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doc('manufacturing', 'doctype', 'bom_operation')
	for d in dataent.db.sql("""select name from `tabBOM` where docstatus < 2""", as_dict=1):
		try:
			bom = dataent.get_doc('BOM', d.name)
			bom.flags.ignore_validate_update_after_submit = True
			bom.calculate_cost()
			bom.save()
			dataent.db.commit()
		except:
			dataent.db.rollback()
