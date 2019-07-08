from __future__ import unicode_literals
import dataent
from dataent.utils import sanitize_html

def execute():
	for product_bundle in dataent.get_all('Product Bundle'):
		doc = dataent.get_doc('Product Bundle', product_bundle.name)
		for item in doc.items:
			if item.description:
				description = sanitize_html(item.description)
				item.db_set('description', description, update_modified=False)
