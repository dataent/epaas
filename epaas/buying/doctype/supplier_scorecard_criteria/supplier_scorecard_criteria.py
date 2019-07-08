# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dataent Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import dataent
from dataent import _
import re
from dataent.model.document import Document

class InvalidFormulaVariable(dataent.ValidationError): pass

class SupplierScorecardCriteria(Document):
	def validate(self):
		self.validate_variables()
		self.validate_formula()

	def validate_variables(self):
		# make sure all the variables exist
		_get_variables(self)

	def validate_formula(self):
		# evaluate the formula with 0's to make sure it is valid
		test_formula = self.formula.replace("\r", "").replace("\n", "")

		regex = r"\{(.*?)\}"

		mylist = re.finditer(regex, test_formula, re.MULTILINE | re.DOTALL)
		for dummy1, match in enumerate(mylist):
			for dummy2 in range(0, len(match.groups())):
				test_formula = test_formula.replace('{' + match.group(1) + '}', "0")

		try:
			dataent.safe_eval(test_formula,  None, {'max':max, 'min': min})
		except Exception:
			dataent.throw(_("Error evaluating the criteria formula"))

@dataent.whitelist()
def get_criteria_list():
	criteria = dataent.db.sql("""
		SELECT
			scs.name
		FROM
			`tabSupplier Scorecard Criteria` scs""",
			{}, as_dict=1)

	return criteria

def get_variables(criteria_name):
	criteria = dataent.get_doc("Supplier Scorecard Criteria", criteria_name)
	return _get_variables(criteria)

def _get_variables(criteria):
	my_variables = []
	regex = r"\{(.*?)\}"

	mylist = re.finditer(regex, criteria.formula, re.MULTILINE | re.DOTALL)
	for dummy1, match in enumerate(mylist):
		for dummy2 in range(0, len(match.groups())):
			try:
				var = dataent.db.sql("""
					SELECT
						scv.variable_label, scv.description, scv.param_name, scv.path
					FROM
						`tabSupplier Scorecard Variable` scv
					WHERE
						param_name=%(param)s""",
						{'param':match.group(1)}, as_dict=1)[0]
				my_variables.append(var)
			except Exception:
				dataent.throw(_('Unable to find variable: ') + str(match.group(1)), InvalidFormulaVariable)

	return my_variables