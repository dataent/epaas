from __future__ import unicode_literals

import dataent
from dataent.model.utils.rename_field import rename_field

def execute():
	for dt, dn in (("Page", "Hub"), ("DocType", "Hub Settings"), ("DocType", "Hub Category")):
		dataent.delete_doc(dt, dn, ignore_missing=True)

	if dataent.db.exists("DocType", "Data Migration Plan"):
		data_migration_plans = dataent.get_all("Data Migration Plan", filters={"module": 'Hub Node'})
		for plan in data_migration_plans:
			plan_doc = dataent.get_doc("Data Migration Plan", plan.name)
			for m in plan_doc.get("mappings"):
				dataent.delete_doc("Data Migration Mapping", m.mapping, force=True)
			docs = dataent.get_all("Data Migration Run", filters={"data_migration_plan": plan.name})
			for doc in docs:
				dataent.delete_doc("Data Migration Run", doc.name)
			dataent.delete_doc("Data Migration Plan", plan.name)
