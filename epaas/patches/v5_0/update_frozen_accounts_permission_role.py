# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

def execute():
	account_settings = dataent.get_doc("Accounts Settings")

	if not account_settings.frozen_accounts_modifier and account_settings.bde_auth_role:
		dataent.db.set_value("Accounts Settings", None,
			"frozen_accounts_modifier", account_settings.bde_auth_role)

