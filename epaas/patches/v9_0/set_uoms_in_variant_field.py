from __future__ import unicode_literals
import dataent


def execute():
	doc = dataent.get_doc('Item Variant Settings')
	variant_field_names = [vf.field_name for vf in doc.fields]
	if 'uoms' not in variant_field_names:
		doc.append(
			'fields', {
					'field_name': 'uoms'
				}
		)
	doc.save()
