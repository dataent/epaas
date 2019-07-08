from __future__ import unicode_literals
import dataent

def execute():
	if 'Manufacturing' in dataent.get_active_domains(): return

	role = 'Manufacturing User'
	dataent.db.set_value('Role', role, 'restrict_to_domain', '')
	dataent.db.set_value('Role', role, 'disabled', 0)

	users = dataent.get_all('Has Role', filters = {
		'parenttype': 'User',
		'role': ('in', ['System Manager', 'Manufacturing Manager'])
	}, fields=['parent'], as_list=1)

	for user in users:
		_user = dataent.get_doc('User', user[0])
		_user.append('roles', {
			'role': role
		})
		_user.flags.ignore_validate = True
		_user.save()
