# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent
from dataent import throw, _
import dataent.defaults
from dataent.utils import cint, flt, get_fullname, cstr
from dataent.contacts.doctype.address.address import get_address_display
from epaas.shopping_cart.doctype.shopping_cart_settings.shopping_cart_settings import get_shopping_cart_settings
from dataent.utils.nestedset import get_root_of
from epaas.accounts.utils import get_account_name
from epaas.utilities.product import get_qty_in_stock


class WebsitePriceListMissingError(dataent.ValidationError):
	pass

def set_cart_count(quotation=None):
	if cint(dataent.db.get_singles_value("Shopping Cart Settings", "enabled")):
		if not quotation:
			quotation = _get_cart_quotation()
		cart_count = cstr(len(quotation.get("items")))

		if hasattr(dataent.local, "cookie_manager"):
			dataent.local.cookie_manager.set_cookie("cart_count", cart_count)

@dataent.whitelist()
def get_cart_quotation(doc=None):
	party = get_party()

	if not doc:
		quotation = _get_cart_quotation(party)
		doc = quotation
		set_cart_count(quotation)

	addresses = get_address_docs(party=party)

	if not doc.customer_address and addresses:
		update_cart_address("customer_address", addresses[0].name)

	return {
		"doc": decorate_quotation_doc(doc),
		"shipping_addresses": [{"name": address.name, "display": address.display}
			for address in addresses],
		"billing_addresses": [{"name": address.name, "display": address.display}
			for address in addresses],
		"shipping_rules": get_applicable_shipping_rules(party)
	}

@dataent.whitelist()
def place_order():
	quotation = _get_cart_quotation()
	cart_settings = dataent.db.get_value("Shopping Cart Settings", None,
		["company", "allow_items_not_in_stock"], as_dict=1)
	quotation.company = cart_settings.company
	if not quotation.get("customer_address"):
		throw(_("{0} is required").format(_(quotation.meta.get_label("customer_address"))))

	quotation.flags.ignore_permissions = True
	quotation.submit()

	if quotation.lead:
		# company used to create customer accounts
		dataent.defaults.set_user_default("company", quotation.company)

	from epaas.selling.doctype.quotation.quotation import _make_sales_order
	sales_order = dataent.get_doc(_make_sales_order(quotation.name, ignore_permissions=True))

	if not cart_settings.allow_items_not_in_stock:
		for item in sales_order.get("items"):
			item.reserved_warehouse, is_stock_item = dataent.db.get_value("Item",
				item.item_code, ["website_warehouse", "is_stock_item"])

			if is_stock_item:
				item_stock = get_qty_in_stock(item.item_code, "website_warehouse")
				if item.qty > item_stock.stock_qty[0][0]:
					throw(_("Only {0} in stock for item {1}").format(item_stock.stock_qty[0][0], item.item_code))

	sales_order.flags.ignore_permissions = True
	sales_order.insert()
	sales_order.submit()

	if hasattr(dataent.local, "cookie_manager"):
		dataent.local.cookie_manager.delete_cookie("cart_count")

	return sales_order.name

@dataent.whitelist()
def update_cart(item_code, qty, with_items=False):
	quotation = _get_cart_quotation()

	empty_card = False
	qty = flt(qty)
	if qty == 0:
		quotation_items = quotation.get("items", {"item_code": ["!=", item_code]})
		if quotation_items:
			quotation.set("items", quotation_items)
		else:
			empty_card = True

	else:
		quotation_items = quotation.get("items", {"item_code": item_code})
		if not quotation_items:
			quotation.append("items", {
				"doctype": "Quotation Item",
				"item_code": item_code,
				"qty": qty
			})
		else:
			quotation_items[0].qty = qty

	apply_cart_settings(quotation=quotation)

	quotation.flags.ignore_permissions = True
	quotation.payment_schedule = []
	if not empty_card:
		quotation.save()
	else:
		quotation.delete()
		quotation = None

	set_cart_count(quotation)

	context = get_cart_quotation(quotation)

	if cint(with_items):
		return {
			"items": dataent.render_template("templates/includes/cart/cart_items.html",
				context),
			"taxes": dataent.render_template("templates/includes/order/order_taxes.html",
				context),
		}
	else:
		return {
			'name': quotation.name,
			'shopping_cart_menu': get_shopping_cart_menu(context)
		}

@dataent.whitelist()
def get_shopping_cart_menu(context=None):
	if not context:
		context = get_cart_quotation()

	return dataent.render_template('templates/includes/cart/cart_dropdown.html', context)

@dataent.whitelist()
def update_cart_address(address_fieldname, address_name):
	quotation = _get_cart_quotation()
	address_display = get_address_display(dataent.get_doc("Address", address_name).as_dict())

	if address_fieldname == "shipping_address_name":
		quotation.shipping_address_name = address_name
		quotation.shipping_address = address_display

		if not quotation.customer_address:
			address_fieldname == "customer_address"

	if address_fieldname == "customer_address":
		quotation.customer_address = address_name
		quotation.address_display = address_display


	apply_cart_settings(quotation=quotation)

	quotation.flags.ignore_permissions = True
	quotation.save()

	context = get_cart_quotation(quotation)
	return {
		"taxes": dataent.render_template("templates/includes/order/order_taxes.html",
			context),
		}

def guess_territory():
	territory = None
	geoip_country = dataent.session.get("session_country")
	if geoip_country:
		territory = dataent.db.get_value("Territory", geoip_country)

	return territory or \
		dataent.db.get_value("Shopping Cart Settings", None, "territory") or \
			get_root_of("Territory")

def decorate_quotation_doc(doc):
	for d in doc.get("items", []):
		d.update(dataent.db.get_value("Item", d.item_code,
			["thumbnail", "website_image", "description", "route"], as_dict=True))

	return doc


def _get_cart_quotation(party=None):
	'''Return the open Quotation of type "Shopping Cart" or make a new one'''
	if not party:
		party = get_party()

	quotation = dataent.get_all("Quotation", fields=["name"], filters=
		{"party_name": party.name, "order_type": "Shopping Cart", "docstatus": 0},
		order_by="modified desc", limit_page_length=1)

	if quotation:
		qdoc = dataent.get_doc("Quotation", quotation[0].name)
	else:
		qdoc = dataent.get_doc({
			"doctype": "Quotation",
			"naming_series": get_shopping_cart_settings().quotation_series or "QTN-CART-",
			"quotation_to": party.doctype,
			"company": dataent.db.get_value("Shopping Cart Settings", None, "company"),
			"order_type": "Shopping Cart",
			"status": "Draft",
			"docstatus": 0,
			"__islocal": 1,
			"party_name": party.name
		})

		qdoc.contact_person = dataent.db.get_value("Contact", {"email_id": dataent.session.user})
		qdoc.contact_email = dataent.session.user

		qdoc.flags.ignore_permissions = True
		qdoc.run_method("set_missing_values")
		apply_cart_settings(party, qdoc)

	return qdoc

def update_party(fullname, company_name=None, mobile_no=None, phone=None):
	party = get_party()

	party.customer_name = company_name or fullname
	party.customer_type == "Company" if company_name else "Individual"

	contact_name = dataent.db.get_value("Contact", {"email_id": dataent.session.user})
	contact = dataent.get_doc("Contact", contact_name)
	contact.first_name = fullname
	contact.last_name = None
	contact.customer_name = party.customer_name
	contact.mobile_no = mobile_no
	contact.phone = phone
	contact.flags.ignore_permissions = True
	contact.save()

	party_doc = dataent.get_doc(party.as_dict())
	party_doc.flags.ignore_permissions = True
	party_doc.save()

	qdoc = _get_cart_quotation(party)
	if not qdoc.get("__islocal"):
		qdoc.customer_name = company_name or fullname
		qdoc.run_method("set_missing_lead_customer_details")
		qdoc.flags.ignore_permissions = True
		qdoc.save()

def apply_cart_settings(party=None, quotation=None):
	if not party:
		party = get_party()
	if not quotation:
		quotation = _get_cart_quotation(party)

	cart_settings = dataent.get_doc("Shopping Cart Settings")

	set_price_list_and_rate(quotation, cart_settings)

	quotation.run_method("calculate_taxes_and_totals")

	set_taxes(quotation, cart_settings)

	_apply_shipping_rule(party, quotation, cart_settings)

def set_price_list_and_rate(quotation, cart_settings):
	"""set price list based on billing territory"""

	_set_price_list(quotation, cart_settings)

	# reset values
	quotation.price_list_currency = quotation.currency = \
		quotation.plc_conversion_rate = quotation.conversion_rate = None
	for item in quotation.get("items"):
		item.price_list_rate = item.discount_percentage = item.rate = item.amount = None

	# refetch values
	quotation.run_method("set_price_list_and_item_details")

	if hasattr(dataent.local, "cookie_manager"):
		# set it in cookies for using in product page
		dataent.local.cookie_manager.set_cookie("selling_price_list", quotation.selling_price_list)

def _set_price_list(quotation, cart_settings):
	"""Set price list based on customer or shopping cart default"""
	if quotation.selling_price_list:
		return

	# check if customer price list exists
	selling_price_list = None
	if quotation.party_name:
		from epaas.accounts.party import get_default_price_list
		selling_price_list = get_default_price_list(dataent.get_doc("Customer", quotation.party_name))

	# else check for territory based price list
	if not selling_price_list:
		selling_price_list = cart_settings.price_list

	quotation.selling_price_list = selling_price_list

def set_taxes(quotation, cart_settings):
	"""set taxes based on billing territory"""
	from epaas.accounts.party import set_taxes

	customer_group = dataent.db.get_value("Customer", quotation.party_name, "customer_group")

	quotation.taxes_and_charges = set_taxes(quotation.party_name, "Customer", \
		quotation.transaction_date, quotation.company, customer_group, None, \
		quotation.customer_address, quotation.shipping_address_name, 1)
#
# 	# clear table
	quotation.set("taxes", [])
#
# 	# append taxes
	quotation.append_taxes_from_master()

def get_party(user=None):
	if not user:
		user = dataent.session.user

	contact_name = dataent.db.get_value("Contact", {"email_id": user})
	party = None

	if contact_name:
		contact = dataent.get_doc('Contact', contact_name)
		if contact.links:
			party_doctype = contact.links[0].link_doctype
			party = contact.links[0].link_name

	cart_settings = dataent.get_doc("Shopping Cart Settings")

	debtors_account = ''

	if cart_settings.enable_checkout:
		debtors_account = get_debtors_account(cart_settings)

	if party:
		return dataent.get_doc(party_doctype, party)

	else:
		if not cart_settings.enabled:
			dataent.local.flags.redirect_location = "/contact"
			raise dataent.Redirect
		customer = dataent.new_doc("Customer")
		fullname = get_fullname(user)
		customer.update({
			"customer_name": fullname,
			"customer_type": "Individual",
			"customer_group": get_shopping_cart_settings().default_customer_group,
			"territory": get_root_of("Territory")
		})

		if debtors_account:
			customer.update({
				"accounts": [{
					"company": cart_settings.company,
					"account": debtors_account
				}]
			})

		customer.flags.ignore_mandatory = True
		customer.insert(ignore_permissions=True)

		contact = dataent.new_doc("Contact")
		contact.update({
			"first_name": fullname,
			"email_id": user
		})
		contact.append('links', dict(link_doctype='Customer', link_name=customer.name))
		contact.flags.ignore_mandatory = True
		contact.insert(ignore_permissions=True)

		return customer

def get_debtors_account(cart_settings):
	payment_gateway_account_currency = \
		dataent.get_doc("Payment Gateway Account", cart_settings.payment_gateway_account).currency

	account_name = _("Debtors ({0})".format(payment_gateway_account_currency))

	debtors_account_name = get_account_name("Receivable", "Asset", is_group=0,\
		account_currency=payment_gateway_account_currency, company=cart_settings.company)

	if not debtors_account_name:
		debtors_account = dataent.get_doc({
			"doctype": "Account",
			"account_type": "Receivable",
			"root_type": "Asset",
			"is_group": 0,
			"parent_account": get_account_name(root_type="Asset", is_group=1, company=cart_settings.company),
			"account_name": account_name,
			"currency": payment_gateway_account_currency
		}).insert(ignore_permissions=True)

		return debtors_account.name

	else:
		return debtors_account_name


def get_address_docs(doctype=None, txt=None, filters=None, limit_start=0, limit_page_length=20,
	party=None):
	if not party:
		party = get_party()

	if not party:
		return []

	address_names = dataent.db.get_all('Dynamic Link', fields=('parent'),
		filters=dict(parenttype='Address', link_doctype=party.doctype, link_name=party.name))

	out = []

	for a in address_names:
		address = dataent.get_doc('Address', a.parent)
		address.display = get_address_display(address.as_dict())
		out.append(address)

	return out

@dataent.whitelist()
def apply_shipping_rule(shipping_rule):
	quotation = _get_cart_quotation()

	quotation.shipping_rule = shipping_rule

	apply_cart_settings(quotation=quotation)

	quotation.flags.ignore_permissions = True
	quotation.save()

	return get_cart_quotation(quotation)

def _apply_shipping_rule(party=None, quotation=None, cart_settings=None):
	if not quotation.shipping_rule:
		shipping_rules = get_shipping_rules(quotation, cart_settings)

		if not shipping_rules:
			return

		elif quotation.shipping_rule not in shipping_rules:
			quotation.shipping_rule = shipping_rules[0]

	if quotation.shipping_rule:
		quotation.run_method("apply_shipping_rule")
		quotation.run_method("calculate_taxes_and_totals")

def get_applicable_shipping_rules(party=None, quotation=None):
	shipping_rules = get_shipping_rules(quotation)

	if shipping_rules:
		rule_label_map = dataent.db.get_values("Shipping Rule", shipping_rules, "label")
		# we need this in sorted order as per the position of the rule in the settings page
		return [[rule, rule_label_map.get(rule)] for rule in shipping_rules]

def get_shipping_rules(quotation=None, cart_settings=None):
	if not quotation:
		quotation = _get_cart_quotation()

	shipping_rules = []
	if quotation.shipping_address_name:
		country = dataent.db.get_value("Address", quotation.shipping_address_name, "country")
		if country:
			shipping_rules = dataent.db.sql_list("""select distinct sr.name
				from `tabShipping Rule Country` src, `tabShipping Rule` sr
				where src.country = %s and
				sr.disabled != 1 and sr.name = src.parent""", country)

	return shipping_rules

def get_address_territory(address_name):
	"""Tries to match city, state and country of address to existing territory"""
	territory = None

	if address_name:
		address_fields = dataent.db.get_value("Address", address_name,
			["city", "state", "country"])
		for value in address_fields:
			territory = dataent.db.get_value("Territory", value)
			if territory:
				break

	return territory

def show_terms(doc):
	return doc.tc_name
