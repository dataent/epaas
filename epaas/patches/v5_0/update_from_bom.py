# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doctype("Stock Entry")
	dataent.db.sql("update `tabStock Entry` set from_bom = if(ifnull(bom_no, '')='', 0, 1)")
