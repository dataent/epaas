from __future__ import unicode_literals
import dataent

def execute():

	dataent.reload_doctype("Opportunity")
	if dataent.db.has_column("Opportunity", "enquiry_from"):
		dataent.db.sql(""" UPDATE `tabOpportunity` set opportunity_from = enquiry_from
			where ifnull(opportunity_from, '') = '' and ifnull(enquiry_from, '') != ''""")

	if dataent.db.has_column("Opportunity", "lead") and dataent.db.has_column("Opportunity", "enquiry_from"):
		dataent.db.sql(""" UPDATE `tabOpportunity` set party_name = lead
			where enquiry_from = 'Lead' and ifnull(party_name, '') = '' and ifnull(lead, '') != ''""")

	if dataent.db.has_column("Opportunity", "customer") and dataent.db.has_column("Opportunity", "enquiry_from"):
		dataent.db.sql(""" UPDATE `tabOpportunity` set party_name = customer
			 where enquiry_from = 'Customer' and ifnull(party_name, '') = '' and ifnull(customer, '') != ''""")
