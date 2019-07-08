from __future__ import unicode_literals
import dataent
from epaas import get_default_currency

def execute():
	dataent.reload_doc("manufacturing", "doctype", "bom")
	dataent.reload_doc("manufacturing", "doctype", "bom_item")
	dataent.reload_doc("manufacturing", "doctype", "bom_explosion_item")
	dataent.reload_doc("manufacturing", "doctype", "bom_operation")
	dataent.reload_doc("manufacturing", "doctype", "bom_scrap_item")

	dataent.db.sql(""" update `tabBOM Operation` set base_hour_rate = hour_rate,
		base_operating_cost = operating_cost """)

	dataent.db.sql(""" update `tabBOM Item` set base_rate = rate, base_amount = amount """)
	dataent.db.sql(""" update `tabBOM Scrap Item` set base_rate = rate, base_amount = amount """)

	dataent.db.sql(""" update `tabBOM` set `tabBOM`.base_operating_cost = `tabBOM`.operating_cost, 
		`tabBOM`.base_raw_material_cost = `tabBOM`.raw_material_cost,
		`tabBOM`.currency = (select default_currency from `tabCompany` where name = `tabBOM`.company)""")
