# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doc("manufacturing", "doctype", "bom")
	dataent.reload_doc("manufacturing", "doctype", "bom_item")
	dataent.reload_doc("manufacturing", "doctype", "bom_explosion_item")
	dataent.reload_doc("manufacturing", "doctype", "bom_operation")

	dataent.db.sql("""update `tabBOM` as bom  set bom.item_name = \
		( select item.item_name from `tabItem` as item  where item.name = bom.item)""")
	dataent.db.sql("""update `tabBOM Item` as bomItem set bomItem.item_name = ( select item.item_name  \
		from `tabItem` as item where item.name = bomItem.item_code)""")
	dataent.db.sql("""update `tabBOM Explosion Item` as explosionItem set explosionItem.item_name = \
		( select item.item_name from `tabItem` as item where item.name = explosionItem.item_code)""")
