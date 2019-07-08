from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doc('setup', 'doctype', 'currency_exchange')
	dataent.db.sql("""update `tabCurrency Exchange` set for_buying = 1, for_selling = 1""")