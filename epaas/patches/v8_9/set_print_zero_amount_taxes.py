from __future__ import unicode_literals
import dataent

from epaas.setup.install import create_print_zero_amount_taxes_custom_field

def execute():
	dataent.reload_doc('printing', 'doctype', 'print_style')
	dataent.reload_doc('printing', 'doctype', 'print_settings')
	create_print_zero_amount_taxes_custom_field()