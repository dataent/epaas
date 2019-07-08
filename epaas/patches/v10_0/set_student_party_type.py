from __future__ import unicode_literals
import dataent

def execute():
	if not dataent.db.exists("Party Type", "Student"):
		party = dataent.new_doc("Party Type")
		party.party_type = "Student"
		party.save()
