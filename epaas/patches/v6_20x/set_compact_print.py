from __future__ import unicode_literals
import dataent

from epaas.setup.install import create_compact_item_print_custom_field

def execute():
	create_compact_item_print_custom_field()
	dataent.db.set_value("Print Settings", None, "compact_item_print", 1)
