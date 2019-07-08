from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doctype("Pricing Rule")

	currency = dataent.db.get_default("currency")
	for doc in dataent.get_all('Pricing Rule', fields = ["company", "name"]):
		if doc.company:
			currency = dataent.get_cached_value('Company',  doc.company,  "default_currency")

		dataent.db.sql("""update `tabPricing Rule` set currency = %s where name = %s""",(currency, doc.name))
