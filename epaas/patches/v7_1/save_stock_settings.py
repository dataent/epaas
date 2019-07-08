from __future__ import unicode_literals
import dataent

def execute():
	stock_settings = dataent.get_doc('Stock Settings')
	
	if stock_settings.default_warehouse \
		and not dataent.db.exists("Warehouse", stock_settings.default_warehouse):
			stock_settings.default_warehouse = None
			
	if stock_settings.stock_uom and not dataent.db.exists("UOM", stock_settings.stock_uom):
		stock_settings.stock_uom = None
		
	stock_settings.flags.ignore_mandatory = True
	stock_settings.save()
