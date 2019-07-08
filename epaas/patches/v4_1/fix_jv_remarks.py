# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

def execute():
	reference_date = guess_reference_date()
	for name in dataent.db.sql_list("""select name from `tabJournal Entry`
			where date(creation)>=%s""", reference_date):
		jv = dataent.get_doc("Journal Entry", name)
		try:
			jv.create_remarks()
		except dataent.MandatoryError:
			pass
		else:
			dataent.db.set_value("Journal Entry", jv.name, "remark", jv.remark)

def guess_reference_date():
	return (dataent.db.get_value("Patch Log", {"patch": "epaas.patches.v4_0.validate_v3_patch"}, "creation")
		or "2014-05-06")
