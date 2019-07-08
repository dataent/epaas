# -*- coding: utf-8 -*-
# Copyright (c) 2018, Dataent Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import dataent
from dataent import _
from dataent.model.document import Document

class DepartmentApprover(Document):
	pass

@dataent.whitelist()
def get_approvers(doctype, txt, searchfield, start, page_len, filters):

	if not filters.get("employee"):
		dataent.throw(_("Please select Employee Record first."))

	approvers = []
	department_details = {}
	department_list = []
	employee_department = filters.get("department") or dataent.get_value("Employee", filters.get("employee"), "department")
	if employee_department:
		department_details = dataent.db.get_value("Department", {"name": employee_department}, ["lft", "rgt"], as_dict=True)
	if department_details:
		department_list = dataent.db.sql("""select name from `tabDepartment` where lft <= %s
			and rgt >= %s
			and disabled=0
			order by lft desc""", (department_details.lft, department_details.rgt), as_list = True)

	if filters.get("doctype") == "Leave Application":
		parentfield = "leave_approvers"
	else:
		parentfield = "expense_approvers"
	if department_list:
		for d in department_list:
			approvers += dataent.db.sql("""select user.name, user.first_name, user.last_name from
				tabUser user, `tabDepartment Approver` approver where
				approver.parent = %s
				and user.name like %s
				and approver.parentfield = %s
				and approver.approver=user.name""",(d, "%" + txt + "%", parentfield), as_list=True)

	return approvers