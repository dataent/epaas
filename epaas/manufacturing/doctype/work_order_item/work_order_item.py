# -*- coding: utf-8 -*-
# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import dataent
from dataent.model.document import Document

class WorkOrderItem(Document):
	pass

def on_doctype_update():
	dataent.db.add_index("Work Order Item", ["item_code", "source_warehouse"])