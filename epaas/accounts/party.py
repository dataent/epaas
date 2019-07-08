# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals

import dataent, epaas
from dataent import _, msgprint, scrub
from dataent.core.doctype.user_permission.user_permission import get_permitted_documents
from dataent.model.utils import get_fetch_values
from dataent.utils import (add_days, getdate, formatdate, date_diff,
	add_years, get_timestamp, nowdate, flt, add_months, get_last_day)
from dataent.contacts.doctype.address.address import (get_address_display,
	get_default_address, get_company_address)
from dataent.contacts.doctype.contact.contact import get_contact_details, get_default_contact
from epaas.exceptions import PartyFrozen, PartyDisabled, InvalidAccountCurrency
from epaas.accounts.utils import get_fiscal_year
from epaas import get_company_currency

from six import iteritems

class DuplicatePartyAccountError(dataent.ValidationError): pass

@dataent.whitelist()
def get_party_details(party=None, account=None, party_type="Customer", company=None, posting_date=None,
	bill_date=None, price_list=None, currency=None, doctype=None, ignore_permissions=False, fetch_payment_terms_template=True,
	party_address=None, shipping_address=None, pos_profile=None):

	if not party:
		return {}
	if not dataent.db.exists(party_type, party):
		dataent.throw(_("{0}: {1} does not exists").format(party_type, party))
	return _get_party_details(party, account, party_type,
		company, posting_date, bill_date, price_list, currency, doctype, ignore_permissions,
		fetch_payment_terms_template, party_address, shipping_address, pos_profile)

def _get_party_details(party=None, account=None, party_type="Customer", company=None, posting_date=None,
	bill_date=None, price_list=None, currency=None, doctype=None, ignore_permissions=False,
	fetch_payment_terms_template=True, party_address=None, shipping_address=None, pos_profile=None):

	out = dataent._dict(set_account_and_due_date(party, account, party_type, company, posting_date, bill_date, doctype))
	party = out[party_type.lower()]

	if not ignore_permissions and not dataent.has_permission(party_type, "read", party):
		dataent.throw(_("Not permitted for {0}").format(party), dataent.PermissionError)

	party = dataent.get_doc(party_type, party)
	currency = party.default_currency if party.get("default_currency") else get_company_currency(company)

	out["taxes_and_charges"] = set_taxes(party.name, party_type, posting_date, company, out.customer_group, out.supplier_group)
	out["payment_terms_template"] = get_pyt_term_template(party.name, party_type, company)
	set_address_details(out, party, party_type, doctype, company, party_address, shipping_address)
	set_contact_details(out, party, party_type)
	set_other_values(out, party, party_type)
	set_price_list(out, party, party_type, price_list, pos_profile)

	out["taxes_and_charges"] = set_taxes(party.name, party_type, posting_date, company, out.customer_group, out.supplier_type)

	if fetch_payment_terms_template:
		out["payment_terms_template"] = get_pyt_term_template(party.name, party_type, company)

	if not out.get("currency"):
		out["currency"] = currency

	# sales team
	if party_type=="Customer":
		out["sales_team"] = [{
			"sales_person": d.sales_person,
			"allocated_percentage": d.allocated_percentage or None
		} for d in party.get("sales_team")]

	# supplier tax withholding category
	if party_type == "Supplier" and party:
		out["supplier_tds"] = dataent.get_value(party_type, party.name, "tax_withholding_category")

	return out

def set_address_details(out, party, party_type, doctype=None, company=None, party_address=None, shipping_address=None):
	billing_address_field = "customer_address" if party_type == "Lead" \
		else party_type.lower() + "_address"
	out[billing_address_field] = party_address or get_default_address(party_type, party.name)
	if doctype:
		out.update(get_fetch_values(doctype, billing_address_field, out[billing_address_field]))
	# address display
	out.address_display = get_address_display(out[billing_address_field])
	# shipping address
	if party_type in ["Customer", "Lead"]:
		out.shipping_address_name = shipping_address or get_party_shipping_address(party_type, party.name)
		out.shipping_address = get_address_display(out["shipping_address_name"])
		if doctype:
			out.update(get_fetch_values(doctype, 'shipping_address_name', out.shipping_address_name))

	if doctype and doctype in ['Delivery Note', 'Sales Invoice']:
		out.update(get_company_address(company))
		if out.company_address:
			out.update(get_fetch_values(doctype, 'company_address', out.company_address))
		get_regional_address_details(out, doctype, company)

	elif doctype and doctype == "Purchase Invoice":
		out.update(get_company_address(company))
		if out.company_address:
			out["shipping_address"] = shipping_address or out["company_address"]
			out.shipping_address_display = get_address_display(out["shipping_address"])
			out.update(get_fetch_values(doctype, 'shipping_address', out.shipping_address))
		get_regional_address_details(out, doctype, company)

@epaas.allow_regional
def get_regional_address_details(out, doctype, company):
	pass

def set_contact_details(out, party, party_type):
	out.contact_person = get_default_contact(party_type, party.name)

	if not out.contact_person:
		out.update({
			"contact_person": None,
			"contact_display": None,
			"contact_email": None,
			"contact_mobile": None,
			"contact_phone": None,
			"contact_designation": None,
			"contact_department": None
		})
	else:
		out.update(get_contact_details(out.contact_person))

def set_other_values(out, party, party_type):
	# copy
	if party_type=="Customer":
		to_copy = ["customer_name", "customer_group", "territory", "language"]
	else:
		to_copy = ["supplier_name", "supplier_group", "language"]
	for f in to_copy:
		out[f] = party.get(f)

	# fields prepended with default in Customer doctype
	for f in ['currency'] \
		+ (['sales_partner', 'commission_rate'] if party_type=="Customer" else []):
		if party.get("default_" + f):
			out[f] = party.get("default_" + f)

def get_default_price_list(party):
	"""Return default price list for party (Document object)"""
	if party.get("default_price_list"):
		return party.default_price_list

	if party.doctype == "Customer":
		price_list =  dataent.get_cached_value("Customer Group",
			party.customer_group, "default_price_list")
		if price_list:
			return price_list

	return None

def set_price_list(out, party, party_type, given_price_list, pos=None):
	# price list
	price_list = get_permitted_documents('Price List')

	if price_list:
		price_list = price_list[0]
	elif pos and party_type == 'Customer':
		customer_price_list = dataent.get_value('Customer', party.name, 'default_price_list')

		if customer_price_list:
			price_list = customer_price_list
		else:
			pos_price_list = dataent.get_value('POS Profile', pos, 'selling_price_list')
			price_list = pos_price_list or given_price_list
	else:
		price_list = get_default_price_list(party) or given_price_list

	if price_list:
		out.price_list_currency = dataent.db.get_value("Price List", price_list, "currency", cache=True)

	out["selling_price_list" if party.doctype=="Customer" else "buying_price_list"] = price_list


def set_account_and_due_date(party, account, party_type, company, posting_date, bill_date, doctype):
	if doctype not in ["Sales Invoice", "Purchase Invoice"]:
		# not an invoice
		return {
			party_type.lower(): party
		}

	if party:
		account = get_party_account(party_type, party, company)

	account_fieldname = "debit_to" if party_type=="Customer" else "credit_to"
	out = {
		party_type.lower(): party,
		account_fieldname : account,
		"due_date": get_due_date(posting_date, party_type, party, company, bill_date)
	}

	return out

@dataent.whitelist()
def get_party_account(party_type, party, company):
	"""Returns the account for the given `party`.
		Will first search in party (Customer / Supplier) record, if not found,
		will search in group (Customer Group / Supplier Group),
		finally will return default."""
	if not company:
		dataent.throw(_("Please select a Company"))

	if not party:
		return

	account = dataent.db.get_value("Party Account",
		{"parenttype": party_type, "parent": party, "company": company}, "account")

	if not account and party_type in ['Customer', 'Supplier']:
		party_group_doctype = "Customer Group" if party_type=="Customer" else "Supplier Group"
		group = dataent.get_cached_value(party_type, party, scrub(party_group_doctype))
		account = dataent.db.get_value("Party Account",
			{"parenttype": party_group_doctype, "parent": group, "company": company}, "account")

	if not account and party_type in ['Customer', 'Supplier']:
		default_account_name = "default_receivable_account" \
			if party_type=="Customer" else "default_payable_account"
		account = dataent.get_cached_value('Company',  company,  default_account_name)

	existing_gle_currency = get_party_gle_currency(party_type, party, company)
	if existing_gle_currency:
		if account:
			account_currency = dataent.db.get_value("Account", account, "account_currency", cache=True)
		if (account and account_currency != existing_gle_currency) or not account:
				account = get_party_gle_account(party_type, party, company)

	return account

@dataent.whitelist()
def get_party_bank_account(party_type, party):
	return dataent.db.get_value('Bank Account', {
		'party_type': party_type,
		'party': party,
		'is_default': 1
	})

def get_party_account_currency(party_type, party, company):
	def generator():
		party_account = get_party_account(party_type, party, company)
		return dataent.db.get_value("Account", party_account, "account_currency", cache=True)

	return dataent.local_cache("party_account_currency", (party_type, party, company), generator)

def get_party_gle_currency(party_type, party, company):
	def generator():
		existing_gle_currency = dataent.db.sql("""select account_currency from `tabGL Entry`
			where docstatus=1 and company=%(company)s and party_type=%(party_type)s and party=%(party)s
			limit 1""", { "company": company, "party_type": party_type, "party": party })

		return existing_gle_currency[0][0] if existing_gle_currency else None

	return dataent.local_cache("party_gle_currency", (party_type, party, company), generator,
		regenerate_if_none=True)

def get_party_gle_account(party_type, party, company):
	def generator():
		existing_gle_account = dataent.db.sql("""select account from `tabGL Entry`
			where docstatus=1 and company=%(company)s and party_type=%(party_type)s and party=%(party)s
			limit 1""", { "company": company, "party_type": party_type, "party": party })

		return existing_gle_account[0][0] if existing_gle_account else None

	return dataent.local_cache("party_gle_account", (party_type, party, company), generator,
		regenerate_if_none=True)

def validate_party_gle_currency(party_type, party, company, party_account_currency=None):
	"""Validate party account currency with existing GL Entry's currency"""
	if not party_account_currency:
		party_account_currency = get_party_account_currency(party_type, party, company)

	existing_gle_currency = get_party_gle_currency(party_type, party, company)

	if existing_gle_currency and party_account_currency != existing_gle_currency:
		dataent.throw(_("Accounting Entry for {0}: {1} can only be made in currency: {2}")
			.format(party_type, party, existing_gle_currency), InvalidAccountCurrency)

def validate_party_accounts(doc):
	companies = []

	for account in doc.get("accounts"):
		if account.company in companies:
			dataent.throw(_("There can only be 1 Account per Company in {0} {1}")
				.format(doc.doctype, doc.name), DuplicatePartyAccountError)
		else:
			companies.append(account.company)

		party_account_currency = dataent.db.get_value("Account", account.account, "account_currency", cache=True)
		existing_gle_currency = get_party_gle_currency(doc.doctype, doc.name, account.company)
		company_default_currency = dataent.get_cached_value('Company',
			dataent.db.get_default("Company"),  "default_currency")

		if existing_gle_currency and party_account_currency != existing_gle_currency:
			dataent.throw(_("Accounting entries have already been made in currency {0} for company {1}. Please select a receivable or payable account with currency {0}.").format(existing_gle_currency, account.company))

		if doc.get("default_currency") and party_account_currency and company_default_currency:
			if doc.default_currency != party_account_currency and doc.default_currency != company_default_currency:
				dataent.throw(_("Billing currency must be equal to either default company's currency or party account currency"))


@dataent.whitelist()
def get_due_date(posting_date, party_type, party, company=None, bill_date=None):
	"""Get due date from `Payment Terms Template`"""
	due_date = None
	if (bill_date or posting_date) and party:
		due_date = bill_date or posting_date
		template_name = get_pyt_term_template(party, party_type, company)

		if template_name:
			due_date = get_due_date_from_template(template_name, posting_date, bill_date).strftime("%Y-%m-%d")
		else:
			if party_type == "Supplier":
				supplier_group = dataent.get_cached_value(party_type, party, "supplier_group")
				template_name = dataent.get_cached_value("Supplier Group", supplier_group, "payment_terms")
				if template_name:
					due_date = get_due_date_from_template(template_name, posting_date, bill_date).strftime("%Y-%m-%d")
	# If due date is calculated from bill_date, check this condition
	if getdate(due_date) < getdate(posting_date):
		due_date = posting_date
	return due_date

def get_due_date_from_template(template_name, posting_date, bill_date):
	"""
	Inspects all `Payment Term`s from the a `Payment Terms Template` and returns the due
	date after considering all the `Payment Term`s requirements.
	:param template_name: Name of the `Payment Terms Template`
	:return: String representing the calculated due date
	"""
	due_date = getdate(bill_date or posting_date)

	template = dataent.get_doc('Payment Terms Template', template_name)

	for term in template.terms:
		if term.due_date_based_on == 'Day(s) after invoice date':
			due_date = max(due_date, add_days(due_date, term.credit_days))
		elif term.due_date_based_on == 'Day(s) after the end of the invoice month':
			due_date = max(due_date, add_days(get_last_day(due_date), term.credit_days))
		else:
			due_date = max(due_date, add_months(get_last_day(due_date), term.credit_months))
	return due_date

def validate_due_date(posting_date, due_date, party_type, party, company=None, bill_date=None, template_name=None):
	if getdate(due_date) < getdate(posting_date):
		dataent.throw(_("Due Date cannot be before Posting / Supplier Invoice Date"))
	else:
		if not template_name: return

		default_due_date = get_due_date_from_template(template_name, posting_date, bill_date).strftime("%Y-%m-%d")

		if not default_due_date:
			return

		if default_due_date != posting_date and getdate(due_date) > getdate(default_due_date):
			is_credit_controller = dataent.db.get_single_value("Accounts Settings", "credit_controller") in dataent.get_roles()
			if is_credit_controller:
				msgprint(_("Note: Due / Reference Date exceeds allowed customer credit days by {0} day(s)")
					.format(date_diff(due_date, default_due_date)))
			else:
				dataent.throw(_("Due / Reference Date cannot be after {0}")
					.format(formatdate(default_due_date)))

@dataent.whitelist()
def set_taxes(party, party_type, posting_date, company, customer_group=None, supplier_group=None,
	billing_address=None, shipping_address=None, use_for_shopping_cart=None):
	from epaas.accounts.doctype.tax_rule.tax_rule import get_tax_template, get_party_details
	args = {
		party_type.lower(): party,
		"company":			company
	}

	if customer_group:
		args['customer_group'] = customer_group

	if supplier_group:
		args['supplier_group'] = supplier_group

	if billing_address or shipping_address:
		args.update(get_party_details(party, party_type, {"billing_address": billing_address, \
			"shipping_address": shipping_address }))
	else:
		args.update(get_party_details(party, party_type))

	if party_type in ("Customer", "Lead"):
		args.update({"tax_type": "Sales"})

		if party_type=='Lead':
			args['customer'] = None
			del args['lead']
	else:
		args.update({"tax_type": "Purchase"})

	if use_for_shopping_cart:
		args.update({"use_for_shopping_cart": use_for_shopping_cart})

	return get_tax_template(posting_date, args)


@dataent.whitelist()
def get_pyt_term_template(party_name, party_type, company=None):
	if party_type not in ("Customer", "Supplier"):
		return
	template = None
	if party_type == 'Customer':
		customer = dataent.get_cached_value("Customer", party_name,
			fieldname=['payment_terms', "customer_group"], as_dict=1)
		template = customer.payment_terms

		if not template and customer.customer_group:
			template = dataent.get_cached_value("Customer Group",
				customer.customer_group, 'payment_terms')
	else:
		supplier = dataent.get_cached_value("Supplier", party_name,
			fieldname=['payment_terms', "supplier_group"], as_dict=1)
		template = supplier.payment_terms
		if not template and supplier.supplier_group:
			template = dataent.get_cached_value("Supplier Group", supplier.supplier_group, 'payment_terms')

	if not template and company:
		template = dataent.get_cached_value('Company',  company,  fieldname='payment_terms')
	return template

def validate_party_frozen_disabled(party_type, party_name):
	if party_type and party_name:
		if party_type in ("Customer", "Supplier"):
			party = dataent.get_cached_value(party_type, party_name, ["is_frozen", "disabled"], as_dict=True)
			if party.disabled:
				dataent.throw(_("{0} {1} is disabled").format(party_type, party_name), PartyDisabled)
			elif party.get("is_frozen"):
				frozen_accounts_modifier = dataent.db.get_single_value( 'Accounts Settings', 'frozen_accounts_modifier')
				if not frozen_accounts_modifier in dataent.get_roles():
					dataent.throw(_("{0} {1} is frozen").format(party_type, party_name), PartyFrozen)

		elif party_type == "Employee":
			if dataent.db.get_value("Employee", party_name, "status") == "Left":
				dataent.msgprint(_("{0} {1} is not active").format(party_type, party_name), alert=True)

def get_timeline_data(doctype, name):
	'''returns timeline data for the past one year'''
	from dataent.desk.form.load import get_communication_data

	out = {}
	fields = 'date(creation), count(name)'
	after = add_years(None, -1).strftime('%Y-%m-%d')
	group_by='group by date(creation)'

	data = get_communication_data(doctype, name,
		fields=fields, after=after, group_by=group_by, as_dict=False)

	# fetch and append data from Activity Log
	data += dataent.db.sql("""select {fields}
		from `tabActivity Log`
		where reference_doctype="{doctype}" and reference_name="{name}"
		and status!='Success' and creation > {after}
		{group_by} order by creation desc
		""".format(doctype=dataent.db.escape(doctype), name=dataent.db.escape(name), fields=fields,
			group_by=group_by, after=after), as_dict=False)

	timeline_items = dict(data)

	for date, count in iteritems(timeline_items):
		timestamp = get_timestamp(date)
		out.update({ timestamp: count })

	return out

def get_dashboard_info(party_type, party, loyalty_program=None):
	current_fiscal_year = get_fiscal_year(nowdate(), as_dict=True)

	doctype = "Sales Invoice" if party_type=="Customer" else "Purchase Invoice"

	companies = dataent.get_all(doctype, filters={
		'docstatus': 1,
		party_type.lower(): party
	}, distinct=1, fields=['company'])

	company_wise_info = []

	company_wise_grand_total = dataent.get_all(doctype,
		filters={
			'docstatus': 1,
			party_type.lower(): party,
			'posting_date': ('between', [current_fiscal_year.year_start_date, current_fiscal_year.year_end_date])
			},
			group_by="company",
			fields=["company", "sum(grand_total) as grand_total", "sum(base_grand_total) as base_grand_total"]
		)

	loyalty_point_details = []

	if party_type == "Customer":
		loyalty_point_details = dataent._dict(dataent.get_all("Loyalty Point Entry",
			filters={
				'customer': party,
				'expiry_date': ('>=', getdate()),
				},
				group_by="company",
				fields=["company", "sum(loyalty_points) as loyalty_points"],
				as_list =1
			))

	company_wise_billing_this_year = dataent._dict()

	for d in company_wise_grand_total:
		company_wise_billing_this_year.setdefault(
			d.company,{
				"grand_total": d.grand_total,
				"base_grand_total": d.base_grand_total
			})


	company_wise_total_unpaid = dataent._dict(dataent.db.sql("""
		select company, sum(debit_in_account_currency) - sum(credit_in_account_currency)
		from `tabGL Entry`
		where party_type = %s and party=%s
		group by company""", (party_type, party)))

	for d in companies:
		company_default_currency = dataent.db.get_value("Company", d.company, 'default_currency')
		party_account_currency = get_party_account_currency(party_type, party, d.company)

		if party_account_currency==company_default_currency:
			billing_this_year = flt(company_wise_billing_this_year.get(d.company,{}).get("base_grand_total"))
		else:
			billing_this_year = flt(company_wise_billing_this_year.get(d.company,{}).get("grand_total"))

		total_unpaid = flt(company_wise_total_unpaid.get(d.company))

		if loyalty_point_details:
			loyalty_points = loyalty_point_details.get(d.company)

		info = {}
		info["billing_this_year"] = flt(billing_this_year) if billing_this_year else 0
		info["currency"] = party_account_currency
		info["total_unpaid"] = flt(total_unpaid) if total_unpaid else 0
		info["company"] = d.company

		if party_type == "Customer" and loyalty_point_details:
			info["loyalty_points"] = loyalty_points

		if party_type == "Supplier":
			info["total_unpaid"] = -1 * info["total_unpaid"]

		company_wise_info.append(info)

	return company_wise_info

def get_party_shipping_address(doctype, name):
	"""
	Returns an Address name (best guess) for the given doctype and name for which `address_type == 'Shipping'` is true.
	and/or `is_shipping_address = 1`.

	It returns an empty string if there is no matching record.

	:param doctype: Party Doctype
	:param name: Party name
	:return: String
	"""
	out = dataent.db.sql(
		'SELECT dl.parent '
		'from `tabDynamic Link` dl join `tabAddress` ta on dl.parent=ta.name '
		'where '
		'dl.link_doctype=%s '
		'and dl.link_name=%s '
		'and dl.parenttype="Address" '
		'and ifnull(ta.disabled, 0) = 0 and'
		'(ta.address_type="Shipping" or ta.is_shipping_address=1) '
		'order by ta.is_shipping_address desc, ta.address_type desc limit 1',
		(doctype, name)
	)
	if out:
		return out[0][0]
	else:
		return ''

def get_partywise_advanced_payment_amount(party_type, posting_date = None):
	cond = "1=1"
	if posting_date:
		cond = "posting_date <= '{0}'".format(posting_date)

	data = dataent.db.sql(""" SELECT party, sum({0}) as amount
		FROM `tabGL Entry`
		WHERE
			party_type = %s and against_voucher is null
			and {1} GROUP BY party"""
		.format(("credit") if party_type == "Customer" else "debit", cond) , party_type)

	if data:
		return dataent._dict(data)