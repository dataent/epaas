# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import print_function, unicode_literals
import dataent

def execute():
	dataent.reload_doc("accounts", "doctype", "account")
	dataent.reload_doc("setup", "doctype", "company")
	dataent.reload_doc("accounts", "doctype", "gl_entry")
	dataent.reload_doc("accounts", "doctype", "journal_entry_account")
	receivable_payable_accounts = create_receivable_payable_account()
	if receivable_payable_accounts:
		set_party_in_jv_and_gl_entry(receivable_payable_accounts)
		delete_individual_party_account()
		remove_customer_supplier_account_report()

def create_receivable_payable_account():
	receivable_payable_accounts = dataent._dict()

	def _create_account(args):
		if args["parent_account"] and dataent.db.exists("Account", args["parent_account"]):
			account_id = dataent.db.get_value("Account", 
					{"account_name": args["account_name"], "company": args["company"]})
			if not account_id:
				account = dataent.new_doc("Account")
				account.is_group = 0
				account.update(args)
				account.insert()
			
				account_id = account.name
			
			dataent.db.set_value("Company", args["company"], ("default_receivable_account"
				if args["account_type"]=="Receivable" else "default_payable_account"), account_id)

			receivable_payable_accounts.setdefault(args["company"], {}).setdefault(args["account_type"], account_id)

	for company in dataent.db.sql_list("select name from tabCompany"):
		_create_account({
				"account_name": "Debtors",
				"account_type": "Receivable",
				"company": company,
				"parent_account": get_parent_account(company, "Customer")
			})

		_create_account({
			"account_name": "Creditors",
			"account_type": "Payable",
			"company": company,
			"parent_account": get_parent_account(company, "Supplier")
		})

	return receivable_payable_accounts

def get_parent_account(company, master_type):
	parent_account = None
	
	if "receivables_group" in dataent.db.get_table_columns("Company"):
		parent_account = dataent.get_cached_value('Company',  company, 
			"receivables_group" if master_type=="Customer" else "payables_group")
	if not parent_account:
		parent_account = dataent.db.get_value("Account", {"company": company,
			"account_name": "Accounts Receivable" if master_type=="Customer" else "Accounts Payable"})

	if not parent_account:
		parent_account = dataent.db.sql_list("""select parent_account from tabAccount
			where company=%s and ifnull(master_type, '')=%s and ifnull(master_name, '')!='' limit 1""",
			(company, master_type))
		parent_account = parent_account[0][0] if parent_account else None

	return parent_account

def set_party_in_jv_and_gl_entry(receivable_payable_accounts):
	accounts = dataent.db.sql("""select name, master_type, master_name, company from `tabAccount`
		where ifnull(master_type, '') in ('Customer', 'Supplier') and ifnull(master_name, '') != ''""", as_dict=1)

	account_map = dataent._dict()
	for d in accounts:
		account_map.setdefault(d.name, d)

	if not account_map:
		return

	for dt in ["Journal Entry Account", "GL Entry"]:
		records = dataent.db.sql("""select name, account from `tab%s` 
			where account in (%s) and ifnull(party, '') = '' and docstatus < 2""" % 
			(dt, ", ".join(['%s']*len(account_map))), tuple(account_map.keys()), as_dict=1)
		for i, d in enumerate(records):
			account_details = account_map.get(d.account, {})
			account_type = "Receivable" if account_details.get("master_type")=="Customer" else "Payable"
			new_account = receivable_payable_accounts[account_details.get("company")][account_type]

			dataent.db.sql("update `tab{0}` set account=%s, party_type=%s, party=%s where name=%s".format(dt),
				(new_account, account_details.get("master_type"), account_details.get("master_name"), d.name))

			if i%500 == 0:
				dataent.db.commit()

def delete_individual_party_account():
	dataent.db.sql("""delete from `tabAccount` 
		where ifnull(master_type, '') in ('Customer', 'Supplier') 
			and ifnull(master_name, '') != '' 
			and not exists(select gle.name from `tabGL Entry` gle 
				where gle.account = tabAccount.name)""")
		
	accounts_not_deleted = dataent.db.sql_list("""select tabAccount.name from `tabAccount` 
		where ifnull(master_type, '') in ('Customer', 'Supplier')
		and ifnull(master_name, '') != '' 
		and exists(select gle.name from `tabGL Entry` gle where gle.account = tabAccount.name)""")
		
	if accounts_not_deleted:
		print("Accounts not deleted: " + "\n".join(accounts_not_deleted))
		

def remove_customer_supplier_account_report():
	for d in ["Customer Account Head", "Supplier Account Head"]:
		dataent.delete_doc("Report", d)
