# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals

import dataent
import dataent.defaults
from epaas.shopping_cart.doctype.shopping_cart_settings.shopping_cart_settings import is_cart_enabled

def show_cart_count():
	if (is_cart_enabled() and
		dataent.db.get_value("User", dataent.session.user, "user_type") == "Website User"):
		return True

	return False

def set_cart_count(login_manager):
	role, parties = check_customer_or_supplier()
	if role == 'Supplier': return
	if show_cart_count():
		from epaas.shopping_cart.cart import set_cart_count
		set_cart_count()

def clear_cart_count(login_manager):
	if show_cart_count():
		dataent.local.cookie_manager.delete_cookie("cart_count")

def update_website_context(context):
	cart_enabled = is_cart_enabled()
	context["shopping_cart_enabled"] = cart_enabled

def check_customer_or_supplier():
	if dataent.session.user:
		contact_name = dataent.get_value("Contact", {"email_id": dataent.session.user})
		if contact_name:
			contact = dataent.get_doc('Contact', contact_name)
			for link in contact.links:
				if link.link_doctype in ('Customer', 'Supplier'):
					return link.link_doctype, link.link_name

		return 'Customer', None