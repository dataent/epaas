# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
import dataent

from dataent.model.document import Document
from dataent.model.rename_doc import bulk_rename

class RenameTool(Document):
	pass

@dataent.whitelist()
def get_doctypes():
	return dataent.db.sql_list("""select name from tabDocType
		where allow_rename=1 and module!='Core' order by name""")

@dataent.whitelist()
def upload(select_doctype=None, rows=None):
	from dataent.utils.csvutils import read_csv_content_from_attached_file
	if not select_doctype:
		select_doctype = dataent.form_dict.select_doctype

	if not dataent.has_permission(select_doctype, "write"):
		raise dataent.PermissionError

	rows = read_csv_content_from_attached_file(dataent.get_doc("Rename Tool", "Rename Tool"))

	return bulk_rename(select_doctype, rows=rows)

