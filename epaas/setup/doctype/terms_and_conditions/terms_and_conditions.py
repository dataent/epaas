# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent
import json
from dataent.model.document import Document
from dataent.utils.jinja import validate_template

from six import string_types

class TermsandConditions(Document):
	def validate(self):
		if self.terms:
			validate_template(self.terms)

@dataent.whitelist()
def get_terms_and_conditions(template_name, doc):
	if isinstance(doc, string_types):
		doc = json.loads(doc)

	terms_and_conditions = dataent.get_doc("Terms and Conditions", template_name)
	
	if terms_and_conditions.terms:
		return dataent.render_template(terms_and_conditions.terms, doc)