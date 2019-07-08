# Copyright (c) 2017, Dataent and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

def execute():
	doctype = 'POS Profile'
	dataent.reload_doctype(doctype)

	for pos in dataent.get_all(doctype, filters={'disabled': 0}):
		doc = dataent.get_doc(doctype, pos.name)

		if not doc.user: continue

		try:
			pos_profile_name = doc.user + ' - ' + doc.company
			doc.flags.ignore_validate  = True
			doc.flags.ignore_mandatory = True
			doc.save()

			dataent.rename_doc(doctype, doc.name, pos_profile_name, force=True)
		except dataent.LinkValidationError:
			dataent.db.set_value("POS Profile", doc.name, 'disabled', 1)
