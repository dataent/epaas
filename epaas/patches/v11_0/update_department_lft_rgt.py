from __future__ import unicode_literals

import dataent
from dataent import _
from dataent.utils.nestedset import rebuild_tree

def execute():
	""" assign lft and rgt appropriately """
	dataent.reload_doc("hr", "doctype", "department")
	if not dataent.db.exists("Department", _('All Departments')):
		dataent.get_doc({
			'doctype': 'Department',
			'department_name': _('All Departments'),
			'is_group': 1
		}).insert(ignore_permissions=True, ignore_mandatory=True)

	dataent.db.sql("""update `tabDepartment` set parent_department = '{0}'
		where is_group = 0""".format(_('All Departments')))

	rebuild_tree("Department", "parent_department")