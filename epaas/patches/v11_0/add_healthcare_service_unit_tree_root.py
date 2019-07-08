from __future__ import unicode_literals
import dataent
from dataent import _

def execute():
	""" assign lft and rgt appropriately """
	if "Healthcare" not in dataent.get_active_domains():
		return

	dataent.reload_doc("healthcare", "doctype", "healthcare_service_unit")
	dataent.reload_doc("healthcare", "doctype", "healthcare_service_unit_type")
	company = dataent.get_value("Company", {"domain": "Healthcare"}, "name")

	if company:
		dataent.get_doc({
			'doctype': 'Healthcare Service Unit',
			'healthcare_service_unit_name': _('All Healthcare Service Units'),
			'is_group': 1,
			'company': company
		}).insert(ignore_permissions=True)

