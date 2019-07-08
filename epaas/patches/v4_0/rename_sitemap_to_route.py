from __future__ import unicode_literals
import dataent
import dataent.model

def execute():
	dataent.reload_doc("setup", "doctype", "item_group")
	dataent.reload_doc("stock", "doctype", "item")
	dataent.reload_doc("setup", "doctype", "sales_partner")
	
	try:
		dataent.model.rename_field("Item Group", "parent_website_sitemap", "parent_website_route")
		dataent.model.rename_field("Item", "parent_website_sitemap", "parent_website_route")
		dataent.model.rename_field("Sales Partner", "parent_website_sitemap",
			 "parent_website_route")
	except Exception as e:
		if e.args[0]!=1054:
			raise
