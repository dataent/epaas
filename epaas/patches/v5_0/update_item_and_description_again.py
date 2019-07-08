# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent
from dataent.utils import cstr
import re

def execute():
	item_details = dataent._dict()
	for d in dataent.db.sql("select name, description from `tabItem`", as_dict=1):
		description = cstr(d.description).strip()
		new_desc = extract_description(description)

		item_details.setdefault(d.name, dataent._dict({
			"old_description": description,
			"new_description": new_desc
		}))


	dt_list= ["Purchase Order Item","Supplier Quotation Item", "BOM", "BOM Explosion Item" , \
	"BOM Item", "Opportunity Item" , "Quotation Item" , "Sales Order Item" , "Delivery Note Item" , \
	"Material Request Item" , "Purchase Receipt Item" , "Stock Entry Detail"]
	for dt in dt_list:
		dataent.reload_doctype(dt)
		records = dataent.db.sql("""select name, `{0}` as item_code, description from `tab{1}`
			where description is not null and description like '%%<table%%'"""
			.format("item" if dt=="BOM" else "item_code", dt), as_dict=1)

		count = 1
		for d in records:
			if d.item_code and item_details.get(d.item_code) \
					and cstr(d.description) == item_details.get(d.item_code).old_description:
				desc = item_details.get(d.item_code).new_description
			else:
				desc = extract_description(cstr(d.description))

			dataent.db.sql("""update `tab{0}` set description = %s
				where name = %s """.format(dt), (desc, d.name))

			count += 1
			if count % 500 == 0:
				dataent.db.commit()


def extract_description(desc):
	for tag in ("img", "table", "tr", "td"):
		desc =  re.sub("\</*{0}[^>]*\>".format(tag), "", desc)

	return desc
