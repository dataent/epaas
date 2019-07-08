# Copyright (c) 2017, Dataent and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent
from dataent.utils.nestedset import rebuild_tree

def execute():
	if not dataent.db.get_value('Asset', {'docstatus': ('<', 2) }, 'name'): return
	dataent.reload_doc('assets', 'doctype', 'location')
	dataent.reload_doc('stock', 'doctype', 'warehouse')

	for d in dataent.get_all('Warehouse',
		fields = ['warehouse_name', 'is_group', 'parent_warehouse'], order_by="lft asc"):
		try:
			loc = dataent.new_doc('Location')
			loc.location_name = d.warehouse_name
			loc.is_group = d.is_group
			loc.flags.ignore_mandatory = True
			if d.parent_warehouse:
				loc.parent_location = get_parent_warehouse_name(d.parent_warehouse)

			loc.save(ignore_permissions=True)
		except dataent.DuplicateEntryError:
			continue

	rebuild_tree("Location", "parent_location")

def get_parent_warehouse_name(warehouse):
	return dataent.db.get_value('Warehouse', warehouse, 'warehouse_name')
			