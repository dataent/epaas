# -*- coding: utf-8 -*-
# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import dataent, json
from dataent.model.document import Document
from dataent import _

class BankGuarantee(Document):
	def validate(self):
		if not (self.customer or self.supplier):
			dataent.throw(_("Select the customer or supplier."))

	def on_submit(self):
		if not self.bank_guarantee_number:
			dataent.throw(_("Enter the Bank Guarantee Number before submittting."))
		if not self.name_of_beneficiary:
			dataent.throw(_("Enter the name of the Beneficiary before submittting."))
		if not self.bank:
			dataent.throw(_("Enter the name of the bank or lending institution before submittting."))

@dataent.whitelist()
def get_vouchar_detials(column_list, doctype, docname):
	return dataent.db.sql(''' select {columns} from `tab{doctype}` where name=%s'''
		.format(columns=", ".join(json.loads(column_list)), doctype=doctype), docname, as_dict=1)[0]
