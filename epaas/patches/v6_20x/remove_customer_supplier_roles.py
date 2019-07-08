from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doc("buying", "doctype", "request_for_quotation_supplier")
	dataent.reload_doc("buying", "doctype", "request_for_quotation_item")
	dataent.reload_doc("buying", "doctype", "request_for_quotation")
	dataent.reload_doc("projects", "doctype", "timesheet")
	
	for role in ('Customer', 'Supplier'):
		dataent.db.sql('''delete from `tabHas Role`
			where role=%s and parent in ("Administrator", "Guest")''', role)

		if not dataent.db.sql('select name from `tabHas Role` where role=%s', role):

			# delete DocPerm
			for doctype in dataent.db.sql('select parent from tabDocPerm where role=%s', role):
				d = dataent.get_doc("DocType", doctype[0])
				d.permissions = [p for p in d.permissions if p.role != role]
				d.save()

			# delete Role
			dataent.delete_doc_if_exists('Role', role)
