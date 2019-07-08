# Copyright (c) 2017, Dataent and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent
from epaas.setup.doctype.company.company import update_company_current_month_sales, update_company_monthly_sales

def execute():
	'''Update company monthly sales history based on sales invoices'''
	dataent.reload_doctype("Company")
	companies = [d['name'] for d in dataent.get_list("Company")]

	for company in companies:
		update_company_current_month_sales(company)
		update_company_monthly_sales(company)
