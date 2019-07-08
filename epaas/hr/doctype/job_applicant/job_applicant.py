# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
from dataent.model.document import Document
import dataent
from dataent import _
from dataent.utils import comma_and, validate_email_add

sender_field = "email_id"

class DuplicationError(dataent.ValidationError): pass

class JobApplicant(Document):
	def onload(self):
		job_offer = dataent.get_all("Job Offer", filters={"job_applicant": self.name})
		if job_offer:
			self.get("__onload").job_offer = job_offer[0].name

	def autoname(self):
		keys = filter(None, (self.applicant_name, self.email_id, self.job_title))
		if not keys:
			dataent.throw(_("Name or Email is mandatory"), dataent.NameError)
		self.name = " - ".join(keys)

	def validate(self):
		self.check_email_id_is_unique()
		if self.email_id:
			validate_email_add(self.email_id, True)

		if not self.applicant_name and self.email_id:
			guess = self.email_id.split('@')[0]
			self.applicant_name = ' '.join([p.capitalize() for p in guess.split('.')])

	def check_email_id_is_unique(self):
		if self.email_id:
			names = dataent.db.sql_list("""select name from `tabJob Applicant`
				where email_id=%s and name!=%s and job_title=%s""", (self.email_id, self.name, self.job_title))

			if names:
				dataent.throw(_("Email Address must be unique, already exists for {0}").format(comma_and(names)), dataent.DuplicateEntryError)

