# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doctype("Quotation")
	dataent.db.sql(""" UPDATE `tabQuotation` set party_name = lead WHERE quotation_to = 'Lead' """)
	dataent.db.sql(""" UPDATE `tabQuotation` set party_name = customer WHERE quotation_to = 'Customer' """)

	dataent.reload_doctype("Opportunity")
	dataent.db.sql(""" UPDATE `tabOpportunity` set party_name = lead WHERE opportunity_from = 'Lead' """)
	dataent.db.sql(""" UPDATE `tabOpportunity` set party_name = customer WHERE opportunity_from = 'Customer' """)