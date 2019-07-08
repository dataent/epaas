from __future__ import unicode_literals
import dataent
from dataent.model.utils.rename_field import rename_field

def execute():
	dataent.reload_doc("stock", "doctype", "item")
	if dataent.db.has_column('Item', 'net_weight'):
		rename_field("Item", "net_weight", "weight_per_unit")
