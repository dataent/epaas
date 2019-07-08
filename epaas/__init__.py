# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import inspect
import dataent
from epaas.hooks import regional_overrides
from dataent.utils import getdate

__version__ = '11.1.44'

def get_default_company(user=None):
	'''Get default company for user'''
	from dataent.defaults import get_user_default_as_list

	if not user:
		user = dataent.session.user

	companies = get_user_default_as_list(user, 'company')
	if companies:
		default_company = companies[0]
	else:
		default_company = dataent.db.get_single_value('Global Defaults', 'default_company')

	return default_company


def get_default_currency():
	'''Returns the currency of the default company'''
	company = get_default_company()
	if company:
		return dataent.get_cached_value('Company',  company,  'default_currency')

def get_default_cost_center(company):
	'''Returns the default cost center of the company'''
	if not company:
		return None

	if not dataent.flags.company_cost_center:
		dataent.flags.company_cost_center = {}
	if not company in dataent.flags.company_cost_center:
		dataent.flags.company_cost_center[company] = dataent.get_cached_value('Company',  company,  'cost_center')
	return dataent.flags.company_cost_center[company]

def get_company_currency(company):
	'''Returns the default company currency'''
	if not dataent.flags.company_currency:
		dataent.flags.company_currency = {}
	if not company in dataent.flags.company_currency:
		dataent.flags.company_currency[company] = dataent.db.get_value('Company',  company,  'default_currency', cache=True)
	return dataent.flags.company_currency[company]

def set_perpetual_inventory(enable=1, company=None):
	if not company:
		company = "_Test Company" if dataent.flags.in_test else get_default_company()

	company = dataent.get_doc("Company", company)
	company.enable_perpetual_inventory = enable
	company.save()

def encode_company_abbr(name, company):
	'''Returns name encoded with company abbreviation'''
	company_abbr = dataent.get_cached_value('Company',  company,  "abbr")
	parts = name.rsplit(" - ", 1)

	if parts[-1].lower() != company_abbr.lower():
		parts.append(company_abbr)

	return " - ".join(parts)

def is_perpetual_inventory_enabled(company):
	if not company:
		company = "_Test Company" if dataent.flags.in_test else get_default_company()

	if not hasattr(dataent.local, 'enable_perpetual_inventory'):
		dataent.local.enable_perpetual_inventory = {}

	if not company in dataent.local.enable_perpetual_inventory:
		dataent.local.enable_perpetual_inventory[company] = dataent.get_cached_value('Company',
			company,  "enable_perpetual_inventory") or 0

	return dataent.local.enable_perpetual_inventory[company]

def get_default_finance_book(company=None):
	if not company:
		company = get_default_company()

	if not hasattr(dataent.local, 'default_finance_book'):
		dataent.local.default_finance_book = {}

	if not company in dataent.local.default_finance_book:
		dataent.local.default_finance_book[company] = dataent.get_cached_value('Company',
			company,  "default_finance_book")

	return dataent.local.default_finance_book[company]

def get_party_account_type(party_type):
	if not hasattr(dataent.local, 'party_account_types'):
		dataent.local.party_account_types = {}

	if not party_type in dataent.local.party_account_types:
		dataent.local.party_account_types[party_type] = dataent.db.get_value("Party Type",
			party_type, "account_type") or ''

	return dataent.local.party_account_types[party_type]

def get_region(company=None):
	'''Return the default country based on flag, company or global settings

	You can also set global company flag in `dataent.flags.company`
	'''
	if company or dataent.flags.company:
		return dataent.get_cached_value('Company',
			company or dataent.flags.company,  'country')
	elif dataent.flags.country:
		return dataent.flags.country
	else:
		return dataent.get_system_settings('country')

def allow_regional(fn):
	'''Decorator to make a function regionally overridable

	Example:
	@epaas.allow_regional
	def myfunction():
	  pass'''
	def caller(*args, **kwargs):
		region = get_region()
		fn_name = inspect.getmodule(fn).__name__ + '.' + fn.__name__
		if region in regional_overrides and fn_name in regional_overrides[region]:
			return dataent.get_attr(regional_overrides[region][fn_name])(*args, **kwargs)
		else:
			return fn(*args, **kwargs)

	return caller

def get_last_membership():
	'''Returns last membership if exists'''
	last_membership = dataent.get_all('Membership', 'name,to_date,membership_type',
		dict(member=dataent.session.user, paid=1), order_by='to_date desc', limit=1)

	return last_membership and last_membership[0]

def is_member():
	'''Returns true if the user is still a member'''
	last_membership = get_last_membership()
	if last_membership and getdate(last_membership.to_date) > getdate():
		return True
	return False