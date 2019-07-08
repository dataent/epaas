# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

from dataent.model.document import Document
from epaas.controllers.print_settings import print_settings_for_item_table

class SalesOrderItem(Document):
	def __setup__(self):
		print_settings_for_item_table(self)

def on_doctype_update():
	dataent.db.add_index("Sales Order Item", ["item_code", "warehouse"])