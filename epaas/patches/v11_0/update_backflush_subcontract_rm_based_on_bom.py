# Copyright (c) 2017, Dataent and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doc('buying', 'doctype', 'buying_settings')
	dataent.db.set_value('Buying Settings', None, 'backflush_raw_materials_of_subcontract_based_on', 'BOM')
	
	dataent.reload_doc('stock', 'doctype', 'stock_entry_detail')
	dataent.db.sql(""" update `tabStock Entry Detail` as sed, 
		`tabStock Entry` as se, `tabPurchase Order Item Supplied` as pois
		set
			sed.subcontracted_item = pois.main_item_code
		where
			se.purpose = 'Subcontract' and sed.parent = se.name
			and pois.rm_item_code = sed.item_code and se.docstatus = 1
			and pois.parenttype = 'Purchase Order'""")