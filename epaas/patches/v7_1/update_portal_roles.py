from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doctype('Role')
	dataent.reload_doctype('User')
	for role_name in ('Customer', 'Supplier', 'Student'):
		if dataent.db.exists('Role', role_name):
			dataent.db.set_value('Role', role_name, 'desk_access', 0)
		else:
			dataent.get_doc(dict(doctype='Role', role_name=role_name, desk_access=0)).insert()


	# set customer, supplier roles
	for c in dataent.get_all('Contact', fields=['user'], filters={'ifnull(user, "")': ('!=', '')}):
		user = dataent.get_doc('User', c.user)
		user.flags.ignore_validate = True
		user.flags.ignore_mandatory = True
		user.save()


