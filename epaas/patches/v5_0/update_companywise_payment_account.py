# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doc('accounts', 'doctype', 'mode_of_payment')
	dataent.reload_doc('accounts', 'doctype', 'mode_of_payment_account')

	mode_of_payment_list = dataent.db.sql("""select name, default_account
		from `tabMode of Payment`""", as_dict=1)

	for d in mode_of_payment_list:
		if d.get("default_account"):
			parent_doc = dataent.get_doc("Mode of Payment", d.get("name"))

			parent_doc.set("accounts",
				[{"company": dataent.db.get_value("Account", d.get("default_account"), "company"),
				"default_account": d.get("default_account")}])
			parent_doc.save()
