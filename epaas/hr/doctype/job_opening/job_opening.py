# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
import dataent

from dataent.website.website_generator import WebsiteGenerator
from dataent import _
from epaas.hr.doctype.staffing_plan.staffing_plan import get_designation_counts, get_active_staffing_plan_details

class JobOpening(WebsiteGenerator):
	website = dataent._dict(
		template = "templates/generators/job_opening.html",
		condition_field = "publish",
		page_title_field = "job_title",
	)

	def validate(self):
		if not self.route:
			self.route = dataent.scrub(self.job_title).replace('_', '-')
		self.validate_current_vacancies()

	def validate_current_vacancies(self):
		if not self.staffing_plan:
			staffing_plan = get_active_staffing_plan_details(self.company,
				self.designation)
			if staffing_plan:
				self.staffing_plan = staffing_plan[0].name
				self.planned_vacancies = staffing_plan[0].vacancies
		elif not self.planned_vacancies:
			planned_vacancies = dataent.db.sql("""
				select vacancies from `tabStaffing Plan Detail`
				where parent=%s and designation=%s""", (self.staffing_plan, self.designation))
			self.planned_vacancies = planned_vacancies[0][0] if planned_vacancies else None

		if self.staffing_plan and self.planned_vacancies:
			staffing_plan_company = dataent.db.get_value("Staffing Plan", self.staffing_plan, "company")
			lft, rgt = dataent.get_cached_value('Company',  staffing_plan_company,  ["lft", "rgt"])

			designation_counts = get_designation_counts(self.designation, self.company)
			current_count = designation_counts['employee_count'] + designation_counts['job_openings']

			if self.planned_vacancies <= current_count:
				dataent.throw(_("Job Openings for designation {0} already open \
					or hiring completed as per Staffing Plan {1}"
					.format(self.designation, self.staffing_plan)))

	def get_context(self, context):
		context.parents = [{'route': 'jobs', 'title': _('All Jobs') }]

def get_list_context(context):
	context.title = _("Jobs")
	context.introduction = _('Current Job Openings')
