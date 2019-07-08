from __future__ import unicode_literals
import dataent
from dataent import _
from dataent.utils.nestedset import rebuild_tree

def execute():
	dataent.local.lang = dataent.db.get_default("lang") or 'en'

	for doctype in ['department', 'leave_period', 'staffing_plan', 'job_opening', 'payroll_entry']:
		dataent.reload_doc("hr", "doctype", doctype)

	companies = dataent.db.get_all("Company", fields=["name", "abbr"])
	departments = dataent.db.get_all("Department")
	comp_dict = {}

	# create a blank list for each company
	for company in companies:
		comp_dict[company.name] = {}

	for department in departments:
		# skip root node
		if _(department.name) == _("All Departments"):
			continue

		# for each company, create a copy of the doc
		department_doc = dataent.get_doc("Department", department)
		for company in companies:
			copy_doc = dataent.copy_doc(department_doc)
			copy_doc.update({"company": company.name})
			try:
				copy_doc.insert()
			except dataent.DuplicateEntryError:
				pass
			# append list of new department for each company
			comp_dict[company.name][department.name] = copy_doc.name

	rebuild_tree('Department', 'parent_department')
	doctypes = ["Asset", "Employee", "Payroll Entry", "Staffing Plan", "Job Opening"]

	for d in doctypes:
		update_records(d, comp_dict)

	update_instructors(comp_dict)

	dataent.local.lang = 'en'

def update_records(doctype, comp_dict):
	when_then = []
	for company in comp_dict:
		records = comp_dict[company]

		for department in records:
			when_then.append('''
				WHEN company = "%s" and department = "%s"
				THEN "%s"
			'''%(company, department, records[department]))

	if not when_then:
		return

	dataent.db.sql("""
		update
			`tab%s`
		set
			department = CASE %s END
	"""%(doctype, " ".join(when_then)))

def update_instructors(comp_dict):
	when_then = []
	emp_details = dataent.get_all("Employee", fields=["name", "company"])

	for employee in emp_details:
		records = comp_dict[employee.company] if employee.company else []

		for department in records:
			when_then.append('''
				WHEN employee = "%s" and department = "%s"
				THEN "%s"
			'''%(employee.name, department, records[department]))

	if not when_then:
		return

	dataent.db.sql("""
		update
			`tabInstructor`
		set
			department = CASE %s END
	"""%(" ".join(when_then)))
