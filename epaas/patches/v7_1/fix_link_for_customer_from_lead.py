from __future__ import unicode_literals
import dataent

def execute():
	for c in dataent.db.sql('select name from tabCustomer where ifnull(lead_name,"")!=""'):
		customer = dataent.get_doc('Customer', c[0])
		customer.update_lead_status()