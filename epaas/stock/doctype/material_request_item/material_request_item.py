# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
import dataent

from epaas.controllers.print_settings import print_settings_for_item_table
from dataent.model.document import Document

class MaterialRequestItem(Document):
	def __setup__(self):
		print_settings_for_item_table(self)

def on_doctype_update():
	dataent.db.add_index("Material Request Item", ["item_code", "warehouse"])