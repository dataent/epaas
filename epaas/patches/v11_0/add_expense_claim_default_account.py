from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doc("setup", "doctype", "company")

	companies = dataent.get_all("Company", fields=["name", "default_payable_account"])

	for company in companies:
		if company.default_payable_account is not None:
			dataent.db.set_value("Company", company.name, "default_expense_claim_payable_account", company.default_payable_account)