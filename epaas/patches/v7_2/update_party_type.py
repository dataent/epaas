# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doc('setup', 'doctype', 'party_type')
	make_party_type()

def make_party_type():
	for party_type in ["Customer", "Supplier", "Employee"]:
		if not dataent.db.get_value("Party Type", party_type):
			doc = dataent.new_doc("Party Type")
			doc.party_type = party_type
			doc.save(ignore_permissions=True)