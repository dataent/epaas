# Copyright (c) 2017, Dataent and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doc('stock', 'doctype', 'item_variant_settings')
	dataent.reload_doc('stock', 'doctype', 'variant_field')

	doc = dataent.get_doc('Item Variant Settings')
	doc.set_default_fields()
	doc.save()