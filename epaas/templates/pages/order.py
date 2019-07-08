# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

from dataent import _
from epaas.shopping_cart.doctype.shopping_cart_settings.shopping_cart_settings import show_attachments

def get_context(context):
	context.no_cache = 1
	context.show_sidebar = True
	context.doc = dataent.get_doc(dataent.form_dict.doctype, dataent.form_dict.name)
	if hasattr(context.doc, "set_indicator"):
		context.doc.set_indicator()

	if show_attachments():
		context.attachments = get_attachments(dataent.form_dict.doctype, dataent.form_dict.name)

	context.parents = dataent.form_dict.parents
	context.title = dataent.form_dict.name
	context.payment_ref = dataent.db.get_value("Payment Request",
		{"reference_name": dataent.form_dict.name}, "name")

	context.enabled_checkout = dataent.get_doc("Shopping Cart Settings").enable_checkout

	default_print_format = dataent.db.get_value('Property Setter', dict(property='default_print_format', doc_type=dataent.form_dict.doctype), "value")
	if default_print_format:
		context.print_format = default_print_format
	else:
		context.print_format = "Standard"

	if not dataent.has_website_permission(context.doc):
		dataent.throw(_("Not Permitted"), dataent.PermissionError)
	
	# check for the loyalty program of the customer
	customer_loyalty_program = dataent.db.get_value("Customer", context.doc.customer, "loyalty_program")	
	if customer_loyalty_program:
		from epaas.accounts.doctype.loyalty_program.loyalty_program import get_loyalty_program_details_with_points
		loyalty_program_details = get_loyalty_program_details_with_points(context.doc.customer, customer_loyalty_program)
		context.available_loyalty_points = int(loyalty_program_details.get("loyalty_points"))

def get_attachments(dt, dn):
        return dataent.get_all("File",
			fields=["name", "file_name", "file_url", "is_private"],
			filters = {"attached_to_name": dn, "attached_to_doctype": dt, "is_private":0})
