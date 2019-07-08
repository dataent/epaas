# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent
from dataent.model.utils.rename_field import rename_field

def execute():
	for dt in ("Sales Invoice Advance", "Purchase Invoice Advance"):
		dataent.reload_doctype(dt)

		dataent.db.sql("update `tab{0}` set reference_type = 'Journal Entry'".format(dt))

		if dataent.get_meta(dt).has_field('journal_entry'):
			rename_field(dt, "journal_entry", "reference_name")

		if dataent.get_meta(dt).has_field('jv_detail_no'):
			rename_field(dt, "jv_detail_no", "reference_row")