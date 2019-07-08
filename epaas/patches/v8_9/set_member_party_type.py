from __future__ import unicode_literals
import dataent

def execute():
	if not dataent.db.exists("Party Type", "Member"):
		dataent.reload_doc("non_profit", "doctype", "member")
		party = dataent.new_doc("Party Type")
		party.party_type = "Member"
		party.save()
