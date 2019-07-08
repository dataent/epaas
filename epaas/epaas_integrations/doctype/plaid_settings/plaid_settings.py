# -*- coding: utf-8 -*-
# Copyright (c) 2018, Dataent Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import dataent
import json
from dataent import _
from dataent.model.document import Document
from epaas.accounts.doctype.journal_entry.journal_entry import get_default_bank_cash_account
from epaas.epaas_integrations.doctype.plaid_settings.plaid_connector import PlaidConnector
from dataent.utils import getdate, formatdate, today, add_months

class PlaidSettings(Document):
	pass

@dataent.whitelist()
def plaid_configuration():
	if dataent.db.get_value("Plaid Settings", None, "enabled") == "1":
		return {"plaid_public_key": dataent.conf.get("plaid_public_key") or None, "plaid_env": dataent.conf.get("plaid_env") or None, "client_name": dataent.local.site }
	else:
		return "disabled"

@dataent.whitelist()
def add_institution(token, response):
	response = json.loads(response)

	plaid = PlaidConnector()
	access_token = plaid.get_access_token(token)

	if not dataent.db.exists("Bank", response["institution"]["name"]):
		try:
			bank = dataent.get_doc({
				"doctype": "Bank",
				"bank_name": response["institution"]["name"],
				"plaid_access_token": access_token
			})
			bank.insert()
		except Exception:
			dataent.throw(dataent.get_traceback())

	else:
		bank = dataent.get_doc("Bank", response["institution"]["name"])
		bank.plaid_access_token = access_token
		bank.save()

	return bank

@dataent.whitelist()
def add_bank_accounts(response, bank, company):
	response = json.loads(response) if not "accounts" in response else response
	bank = json.loads(bank)
	result = []

	default_gl_account = get_default_bank_cash_account(company, "Bank")
	if not default_gl_account:
		dataent.throw(_("Please setup a default bank account for company {0}".format(company)))

	for account in response["accounts"]:
		acc_type = dataent.db.get_value("Account Type", account["type"])
		if not acc_type:
			add_account_type(account["type"])

		acc_subtype = dataent.db.get_value("Account Subtype", account["subtype"])
		if not acc_subtype:
			add_account_subtype(account["subtype"])

		if not dataent.db.exists("Bank Account", dict(integration_id=account["id"])):
			try:
				new_account = dataent.get_doc({
					"doctype": "Bank Account",
					"bank": bank["bank_name"],
					"account": default_gl_account.account,
					"account_name": account["name"],
					"account_type": account["type"] or "",
					"account_subtype": account["subtype"] or "",
					"mask": account["mask"] or "",
					"integration_id": account["id"],
					"is_company_account": 1,
					"company": company
				})
				new_account.insert()

				result.append(new_account.name)

			except dataent.UniqueValidationError:
				dataent.msgprint(_("Bank account {0} already exists and could not be created again").format(new_account.account_name))
			except Exception:
				dataent.throw(dataent.get_traceback())

		else:
			result.append(dataent.db.get_value("Bank Account", dict(integration_id=account["id"]), "name"))

	return result

def add_account_type(account_type):
	try:
		dataent.get_doc({
			"doctype": "Account Type",
			"account_type": account_type
		}).insert()
	except Exception:
		dataent.throw(dataent.get_traceback())


def add_account_subtype(account_subtype):
	try:
		dataent.get_doc({
			"doctype": "Account Subtype",
			"account_subtype": account_subtype
		}).insert()
	except Exception:
		dataent.throw(dataent.get_traceback())

@dataent.whitelist()
def sync_transactions(bank, bank_account):

	last_sync_date = dataent.db.get_value("Bank Account", bank_account, "last_integration_date")
	if last_sync_date:
		start_date = formatdate(last_sync_date, "YYYY-MM-dd")
	else:
		start_date = formatdate(add_months(today(), -12), "YYYY-MM-dd")
	end_date = formatdate(today(), "YYYY-MM-dd")

	try:
		transactions = get_transactions(bank=bank, bank_account=bank_account, start_date=start_date, end_date=end_date)
		result = []
		if transactions:
			for transaction in transactions:
				result.append(new_bank_transaction(transaction))

		dataent.db.set_value("Bank Account", bank_account, "last_integration_date", getdate(end_date))

		return result
	except Exception:
		dataent.log_error(dataent.get_traceback(), _("Plaid transactions sync error"))

def get_transactions(bank, bank_account=None, start_date=None, end_date=None):
	access_token = None

	if bank_account:
		related_bank = dataent.db.get_values("Bank Account", bank_account, ["bank", "integration_id"], as_dict=True)
		access_token = dataent.db.get_value("Bank", related_bank[0].bank, "plaid_access_token")
		account_id = related_bank[0].integration_id

	else:
		access_token = dataent.db.get_value("Bank", bank, "plaid_access_token")
		account_id = None

	plaid = PlaidConnector(access_token)
	transactions = plaid.get_transactions(start_date=start_date, end_date=end_date, account_id=account_id)

	return transactions

def new_bank_transaction(transaction):
	result = []

	bank_account = dataent.db.get_value("Bank Account", dict(integration_id=transaction["account_id"]))

	if float(transaction["amount"]) >= 0:
		debit = float(transaction["amount"])
		credit = 0
	else:
		debit = 0
		credit = abs(float(transaction["amount"]))

	status = "Pending" if transaction["pending"] == "True" else "Settled"

	if not dataent.db.exists("Bank Transaction", dict(transaction_id=transaction["transaction_id"])):
		try:
			new_transaction = dataent.get_doc({
				"doctype": "Bank Transaction",
				"date": getdate(transaction["date"]),
				"status": status,
				"bank_account": bank_account,
				"debit": debit,
				"credit": credit,
				"currency": transaction["iso_currency_code"],
				"description": transaction["name"]
			})
			new_transaction.insert()
			new_transaction.submit()

			result.append(new_transaction.name)

		except Exception:
			dataent.throw(dataent.get_traceback())

	return result

def automatic_synchronization():
	settings = dataent.get_doc("Plaid Settings", "Plaid Settings")

	if settings.enabled == 1 and settings.automatic_sync == 1:
		plaid_accounts = dataent.get_all("Bank Account", filter={"integration_id": ["!=", ""]}, fields=["name", "bank"])

		for plaid_account in plaid_accounts:
			dataent.enqueue("epaas.epaas_integrations.doctype.plaid_settings.plaid_settings.sync_transactions", bank=plaid_account.bank, bank_account=plaid_account.name)
