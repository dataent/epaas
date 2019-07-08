from __future__ import unicode_literals
import dataent
from dataent.model.utils.rename_field import rename_field

def execute():
	dataent.reload_doc("setup", "doctype", "company")
	if dataent.db.has_column('Company', 'sales_target'):
		rename_field("Company", "sales_target", "monthly_sales_target")
