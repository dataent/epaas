from __future__ import unicode_literals
import dataent
from dataent.core.doctype.dynamic_link.dynamic_link import deduplicate_dynamic_links
from dataent.utils import update_progress_bar

def execute():
	dataent.reload_doc('core', 'doctype', 'dynamic_link')
	dataent.reload_doc('contacts', 'doctype', 'contact')
	dataent.reload_doc('contacts', 'doctype', 'address')
	map_fields = (
		('Customer', 'customer'),
		('Supplier', 'supplier'),
		('Lead', 'lead'),
		('Sales Partner', 'sales_partner')
	)
	for doctype in ('Contact', 'Address'):
		if dataent.db.has_column(doctype, 'customer'):
			items = dataent.get_all(doctype)
			for i, doc in enumerate(items):
				doc = dataent.get_doc(doctype, doc.name)
				dirty = False
				for field in map_fields:
					if doc.get(field[1]):
						doc.append('links', dict(link_doctype=field[0], link_name=doc.get(field[1])))
						dirty = True

					if dirty:
						deduplicate_dynamic_links(doc)
						doc.update_children()

					update_progress_bar('Updating {0}'.format(doctype), i, len(items))
			print