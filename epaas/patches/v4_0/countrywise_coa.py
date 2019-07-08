# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doc("setup", 'doctype', "company")
	dataent.reload_doc("accounts", 'doctype', "account")

	dataent.db.sql("""update tabAccount set account_type='Cash'
		where account_type='Bank or Cash' and account_name in ('Cash', 'Cash In Hand')""")

	dataent.db.sql("""update tabAccount set account_type='Stock'
		where account_name = 'Stock Assets'""")

	ac_types = {"Fixed Asset Account": "Fixed Asset", "Bank or Cash": "Bank"}
	for old, new in ac_types.items():
		dataent.db.sql("""update tabAccount set account_type=%s
			where account_type=%s""", (new, old))

	try:
		dataent.db.sql("""update `tabAccount` set report_type =
			if(is_pl_account='Yes', 'Profit and Loss', 'Balance Sheet')""")

		dataent.db.sql("""update `tabAccount` set balance_must_be=debit_or_credit
			where ifnull(allow_negative_balance, 0) = 0""")
	except:
		pass
