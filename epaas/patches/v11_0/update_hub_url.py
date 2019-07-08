from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doc('hub_node', 'doctype', 'Marketplace Settings')
	dataent.db.set_value('Marketplace Settings', 'Marketplace Settings', 'marketplace_url', 'https://hubmarket.org')
