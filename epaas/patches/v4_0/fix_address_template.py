# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors

from __future__ import unicode_literals
import dataent

def execute():
	missing_line = """{{ address_line1 }}<br>"""
	for name, template in dataent.db.sql("select name, template from `tabAddress Template`"):
		if missing_line not in template:
			d = dataent.get_doc("Address Template", name)
			d.template = missing_line + d.template
			d.save()
