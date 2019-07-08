# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import dataent
from dataent.model.document import Document
from dataent.model.mapper import get_mapped_doc

class JobOffer(Document):
	def onload(self):
		employee = dataent.db.get_value("Employee", {"job_applicant": self.job_applicant}, "name") or ""
		self.set_onload("employee", employee)

@dataent.whitelist()
def make_employee(source_name, target_doc=None):
	def set_missing_values(source, target):
		target.personal_email = dataent.db.get_value("Job Applicant", source.job_applicant, "email_id")
	doc = get_mapped_doc("Job Offer", source_name, {
			"Job Offer": {
				"doctype": "Employee",
				"field_map": {
					"applicant_name": "employee_name",
				}}
		}, target_doc, set_missing_values)
	return doc

