# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent, epaas

import json
from dataent import _
from dataent.utils import flt
from epaas.setup.doctype.setup_progress.setup_progress import update_domain_actions, get_domain_actions_state

@dataent.whitelist()
def set_sales_target(args_data):
	args = json.loads(args_data)
	defaults = dataent.defaults.get_defaults()
	dataent.db.set_value("Company", defaults.get("company"), "monthly_sales_target", args.get('monthly_sales_target'))

@dataent.whitelist()
def create_customers(args_data):
	args = json.loads(args_data)
	defaults = dataent.defaults.get_defaults()
	for i in range(1,4):
		customer = args.get("customer_" + str(i))
		if customer:
			try:
				doc = dataent.get_doc({
					"doctype":"Customer",
					"customer_name": customer,
					"customer_type": "Company",
					"customer_group": _("Commercial"),
					"territory": defaults.get("country"),
					"company": defaults.get("company")
				}).insert()

				if args.get("customer_contact_" + str(i)):
					create_contact(args.get("customer_contact_" + str(i)),
						"Customer", doc.name)
			except dataent.NameError:
				pass

@dataent.whitelist()
def create_letterhead(args_data):
	args = json.loads(args_data)
	letterhead = args.get("letterhead")
	if letterhead:
		try:
			dataent.get_doc({
					"doctype":"Letter Head",
					"content":"""<div><img src="{0}" style='max-width: 100%%;'><br></div>""".format(letterhead.encode('utf-8')),
					"letter_head_name": _("Standard"),
					"is_default": 1
			}).insert()
		except dataent.NameError:
			pass

@dataent.whitelist()
def create_suppliers(args_data):
	args = json.loads(args_data)
	defaults = dataent.defaults.get_defaults()
	for i in range(1,4):
		supplier = args.get("supplier_" + str(i))
		if supplier:
			try:
				doc = dataent.get_doc({
					"doctype":"Supplier",
					"supplier_name": supplier,
					"supplier_group": _("Local"),
					"company": defaults.get("company")
				}).insert()

				if args.get("supplier_contact_" + str(i)):
					create_contact(args.get("supplier_contact_" + str(i)),
						"Supplier", doc.name)
			except dataent.NameError:
				pass

def create_contact(contact, party_type, party):
	"""Create contact based on given contact name"""
	contact = contact	.split(" ")

	contact = dataent.get_doc({
		"doctype":"Contact",
		"first_name":contact[0],
		"last_name": len(contact) > 1 and contact[1] or ""
	})
	contact.append('links', dict(link_doctype=party_type, link_name=party))
	contact.insert()

@dataent.whitelist()
def create_items(args_data):
	args = json.loads(args_data)
	defaults = dataent.defaults.get_defaults()
	for i in range(1,4):
		item = args.get("item_" + str(i))
		if item:
			default_warehouse = ""
			default_warehouse = dataent.db.get_value("Warehouse", filters={
				"warehouse_name": _("Finished Goods"),
				"company": defaults.get("company_name")
			})

			try:
				dataent.get_doc({
					"doctype":"Item",
					"item_code": item,
					"item_name": item,
					"description": item,
					"show_in_website": 1,
					"is_sales_item": 1,
					"is_purchase_item": 1,
					"is_stock_item": 1,
					"item_group": _("Products"),
					"stock_uom": _(args.get("item_uom_" + str(i))),
					"item_defaults": [{
						"default_warehouse": default_warehouse,
						"company": defaults.get("company_name")
					}]
				}).insert()

			except dataent.NameError:
				pass
			else:
				if args.get("item_price_" + str(i)):
					item_price = flt(args.get("item_price_" + str(i)))

					price_list_name = dataent.db.get_value("Price List", {"selling": 1})
					make_item_price(item, price_list_name, item_price)
					price_list_name = dataent.db.get_value("Price List", {"buying": 1})
					make_item_price(item, price_list_name, item_price)


def make_item_price(item, price_list_name, item_price):
	dataent.get_doc({
		"doctype": "Item Price",
		"price_list": price_list_name,
		"item_code": item,
		"price_list_rate": item_price
	}).insert()

# Education
@dataent.whitelist()
def create_program(args_data):
	args = json.loads(args_data)
	for i in range(1,4):
		if args.get("program_" + str(i)):
			program = dataent.new_doc("Program")
			program.program_code = args.get("program_" + str(i))
			program.program_name = args.get("program_" + str(i))
			try:
				program.save()
			except dataent.DuplicateEntryError:
				pass

@dataent.whitelist()
def create_course(args_data):
	args = json.loads(args_data)
	for i in range(1,4):
		if args.get("course_" + str(i)):
			course = dataent.new_doc("Course")
			course.course_code = args.get("course_" + str(i))
			course.course_name = args.get("course_" + str(i))
			try:
				course.save()
			except dataent.DuplicateEntryError:
				pass

@dataent.whitelist()
def create_instructor(args_data):
	args = json.loads(args_data)
	for i in range(1,4):
		if args.get("instructor_" + str(i)):
			instructor = dataent.new_doc("Instructor")
			instructor.instructor_name = args.get("instructor_" + str(i))
			try:
				instructor.save()
			except dataent.DuplicateEntryError:
				pass

@dataent.whitelist()
def create_room(args_data):
	args = json.loads(args_data)
	for i in range(1,4):
		if args.get("room_" + str(i)):
			room = dataent.new_doc("Room")
			room.room_name = args.get("room_" + str(i))
			room.seating_capacity = args.get("room_capacity_" + str(i))
			try:
				room.save()
			except dataent.DuplicateEntryError:
				pass

@dataent.whitelist()
def create_users(args_data):
	if dataent.session.user == 'Administrator':
		return
	args = json.loads(args_data)
	defaults = dataent.defaults.get_defaults()
	for i in range(1,4):
		email = args.get("user_email_" + str(i))
		fullname = args.get("user_fullname_" + str(i))
		if email:
			if not fullname:
				fullname = email.split("@")[0]

			parts = fullname.split(" ", 1)

			user = dataent.get_doc({
				"doctype": "User",
				"email": email,
				"first_name": parts[0],
				"last_name": parts[1] if len(parts) > 1 else "",
				"enabled": 1,
				"user_type": "System User"
			})

			# default roles
			user.append_roles("Projects User", "Stock User", "Support Team")
			user.flags.delay_emails = True

			if not dataent.db.get_value("User", email):
				user.insert(ignore_permissions=True)

				# create employee
				emp = dataent.get_doc({
					"doctype": "Employee",
					"employee_name": fullname,
					"user_id": email,
					"status": "Active",
					"company": defaults.get("company")
				})
				emp.flags.ignore_mandatory = True
				emp.insert(ignore_permissions = True)

# Ennumerate the setup hooks you're going to need, apart from the slides

@dataent.whitelist()
def update_default_domain_actions_and_get_state():
	domain = dataent.get_cached_value('Company',  epaas.get_default_company(),  'domain')
	update_domain_actions(domain)
	return get_domain_actions_state(domain)
