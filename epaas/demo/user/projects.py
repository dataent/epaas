# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals

import dataent, epaas
from dataent.utils import flt
from dataent.utils.make_random import get_random
from epaas.projects.doctype.timesheet.test_timesheet import make_timesheet
from epaas.demo.user.hr import make_sales_invoice_for_timesheet

def run_projects(current_date):
	dataent.set_user(dataent.db.get_global('demo_projects_user'))
	if dataent.db.get_global('demo_projects_user'):
		make_project(current_date)
		make_timesheet_for_projects(current_date)
		close_tasks(current_date)

def make_timesheet_for_projects(current_date	):
	for data in dataent.get_all("Task", ["name", "project"], {"status": "Open", "exp_end_date": ("<", current_date)}):
		employee = get_random("Employee")
		ts = make_timesheet(employee, simulate = True, billable = 1, company = epaas.get_default_company(),
			activity_type=get_random("Activity Type"), project=data.project, task =data.name)

		if flt(ts.total_billable_amount) > 0.0:
			make_sales_invoice_for_timesheet(ts.name)
			dataent.db.commit()

def close_tasks(current_date):
	for task in dataent.get_all("Task", ["name"], {"status": "Open", "exp_end_date": ("<", current_date)}):
		task = dataent.get_doc("Task", task.name)
		task.status = "Closed"
		task.save()

def make_project(current_date):
	if not dataent.db.exists('Project', 
		"New Product Development " + current_date.strftime("%Y-%m-%d")):
		project = dataent.get_doc({
			"doctype": "Project",
			"project_name": "New Product Development " + current_date.strftime("%Y-%m-%d"),
		})
		project.set("tasks", [
				{
					"title": "Review Requirements",
					"start_date": dataent.utils.add_days(current_date, 10),
					"end_date": dataent.utils.add_days(current_date, 11)
				},
				{
					"title": "Design Options",
					"start_date": dataent.utils.add_days(current_date, 11),
					"end_date": dataent.utils.add_days(current_date, 20)
				},
				{
					"title": "Make Prototypes",
					"start_date": dataent.utils.add_days(current_date, 20),
					"end_date": dataent.utils.add_days(current_date, 30)
				},
				{
					"title": "Customer Feedback on Prototypes",
					"start_date": dataent.utils.add_days(current_date, 30),
					"end_date": dataent.utils.add_days(current_date, 40)
				},
				{
					"title": "Freeze Feature Set",
					"start_date": dataent.utils.add_days(current_date, 40),
					"end_date": dataent.utils.add_days(current_date, 45)
				},
				{
					"title": "Testing",
					"start_date": dataent.utils.add_days(current_date, 45),
					"end_date": dataent.utils.add_days(current_date, 60)
				},
				{
					"title": "Product Engineering",
					"start_date": dataent.utils.add_days(current_date, 45),
					"end_date": dataent.utils.add_days(current_date, 55)
				},
				{
					"title": "Supplier Contracts",
					"start_date": dataent.utils.add_days(current_date, 55),
					"end_date": dataent.utils.add_days(current_date, 70)
				},
				{
					"title": "Design and Build Fixtures",
					"start_date": dataent.utils.add_days(current_date, 45),
					"end_date": dataent.utils.add_days(current_date, 65)
				},
				{
					"title": "Test Run",
					"start_date": dataent.utils.add_days(current_date, 70),
					"end_date": dataent.utils.add_days(current_date, 80)
				},
				{
					"title": "Launch",
					"start_date": dataent.utils.add_days(current_date, 80),
					"end_date": dataent.utils.add_days(current_date, 90)
				},
			])
		project.insert()
