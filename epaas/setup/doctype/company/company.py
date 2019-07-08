# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent, os, json
from dataent import _
from dataent.utils import get_timestamp

from dataent.utils import cint, today, formatdate
import dataent.defaults
from dataent.cache_manager import clear_defaults_cache

from dataent.model.document import Document
from dataent.contacts.address_and_contact import load_address_and_contact
from dataent.utils.nestedset import NestedSet

class Company(NestedSet):
	nsm_parent_field = 'parent_company'

	def onload(self):
		load_address_and_contact(self, "company")
		self.get("__onload")["transactions_exist"] = self.check_if_transactions_exist()

	def check_if_transactions_exist(self):
		exists = False
		for doctype in ["Sales Invoice", "Delivery Note", "Sales Order", "Quotation",
			"Purchase Invoice", "Purchase Receipt", "Purchase Order", "Supplier Quotation"]:
				if dataent.db.sql("""select name from `tab%s` where company=%s and docstatus=1
					limit 1""" % (doctype, "%s"), self.name):
						exists = True
						break

		return exists

	def validate(self):
		self.validate_abbr()
		self.validate_default_accounts()
		self.validate_currency()
		self.validate_coa_input()
		self.validate_perpetual_inventory()
		self.check_country_change()
		self.set_chart_of_accounts()

	def validate_abbr(self):
		if not self.abbr:
			self.abbr = ''.join([c[0] for c in self.company_name.split()]).upper()

		self.abbr = self.abbr.strip()

		# if self.get('__islocal') and len(self.abbr) > 5:
		# 	dataent.throw(_("Abbreviation cannot have more than 5 characters"))

		if not self.abbr.strip():
			dataent.throw(_("Abbreviation is mandatory"))

		if dataent.db.sql("select abbr from tabCompany where name!=%s and abbr=%s", (self.name, self.abbr)):
			dataent.throw(_("Abbreviation already used for another company"))

	def create_default_tax_template(self):
		from epaas.setup.setup_wizard.operations.taxes_setup import create_sales_tax
		create_sales_tax({
			'country': self.country,
			'company_name': self.name
		})

	def validate_default_accounts(self):
		for field in ["default_bank_account", "default_cash_account",
			"default_receivable_account", "default_payable_account",
			"default_expense_account", "default_income_account",
			"stock_received_but_not_billed", "stock_adjustment_account",
			"expenses_included_in_valuation", "default_payroll_payable_account"]:
				if self.get(field):
					for_company = dataent.db.get_value("Account", self.get(field), "company")
					if for_company != self.name:
						dataent.throw(_("Account {0} does not belong to company: {1}")
							.format(self.get(field), self.name))

	def validate_currency(self):
		if self.is_new():
			return
		self.previous_default_currency = dataent.get_cached_value('Company',  self.name,  "default_currency")
		if self.default_currency and self.previous_default_currency and \
			self.default_currency != self.previous_default_currency and \
			self.check_if_transactions_exist():
				dataent.throw(_("Cannot change company's default currency, because there are existing transactions. Transactions must be cancelled to change the default currency."))

	def on_update(self):
		NestedSet.on_update(self)
		if not dataent.db.sql("""select name from tabAccount
				where company=%s and docstatus<2 limit 1""", self.name):
			if not dataent.local.flags.ignore_chart_of_accounts:
				dataent.flags.country_change = True
				self.create_default_accounts()
				self.create_default_warehouses()

		if dataent.flags.country_change:
			install_country_fixtures(self.name)
			self.create_default_tax_template()



		if not dataent.db.get_value("Department", {"company": self.name}):
			from epaas.setup.setup_wizard.operations.install_fixtures import install_post_company_fixtures
			install_post_company_fixtures(dataent._dict({'company_name': self.name}))

		if not dataent.db.get_value("Cost Center", {"is_group": 0, "company": self.name}):
			self.create_default_cost_center()

		if not dataent.local.flags.ignore_chart_of_accounts:
			self.set_default_accounts()
			if self.default_cash_account:
				self.set_mode_of_payment_account()

		if self.default_currency:
			dataent.db.set_value("Currency", self.default_currency, "enabled", 1)

		if hasattr(dataent.local, 'enable_perpetual_inventory') and \
			self.name in dataent.local.enable_perpetual_inventory:
			dataent.local.enable_perpetual_inventory[self.name] = self.enable_perpetual_inventory

		dataent.clear_cache()

	def create_default_warehouses(self):
		for wh_detail in [
			{"warehouse_name": _("All Warehouses"), "is_group": 1},
			{"warehouse_name": _("Stores"), "is_group": 0},
			{"warehouse_name": _("Work In Progress"), "is_group": 0},
			{"warehouse_name": _("Finished Goods"), "is_group": 0}]:

			if not dataent.db.exists("Warehouse", "{0} - {1}".format(wh_detail["warehouse_name"], self.abbr)):
				warehouse = dataent.get_doc({
					"doctype":"Warehouse",
					"warehouse_name": wh_detail["warehouse_name"],
					"is_group": wh_detail["is_group"],
					"company": self.name,
					"parent_warehouse": "{0} - {1}".format(_("All Warehouses"), self.abbr) \
						if not wh_detail["is_group"] else ""
				})
				warehouse.flags.ignore_permissions = True
				warehouse.flags.ignore_mandatory = True
				warehouse.insert()

	def create_default_accounts(self):
		from epaas.accounts.doctype.account.chart_of_accounts.chart_of_accounts import create_charts
		dataent.local.flags.ignore_root_company_validation = True
		create_charts(self.name, self.chart_of_accounts, self.existing_company)

		dataent.db.set(self, "default_receivable_account", dataent.db.get_value("Account",
			{"company": self.name, "account_type": "Receivable", "is_group": 0}))
		dataent.db.set(self, "default_payable_account", dataent.db.get_value("Account",
			{"company": self.name, "account_type": "Payable", "is_group": 0}))

	def validate_coa_input(self):
		if self.create_chart_of_accounts_based_on == "Existing Company":
			self.chart_of_accounts = None
			if not self.existing_company:
				dataent.throw(_("Please select Existing Company for creating Chart of Accounts"))

		else:
			self.existing_company = None
			self.create_chart_of_accounts_based_on = "Standard Template"
			if not self.chart_of_accounts:
				self.chart_of_accounts = "Standard"

	def validate_perpetual_inventory(self):
		if not self.get("__islocal"):
			if cint(self.enable_perpetual_inventory) == 1 and not self.default_inventory_account:
				dataent.msgprint(_("Set default inventory account for perpetual inventory"),
					alert=True, indicator='orange')

	def check_country_change(self):
		dataent.flags.country_change = False

		if not self.get('__islocal') and \
			self.country != dataent.get_cached_value('Company',  self.name,  'country'):
			dataent.flags.country_change = True

	def set_chart_of_accounts(self):
		''' If parent company is set, chart of accounts will be based on that company '''
		if self.parent_company:
			self.create_chart_of_accounts_based_on = "Existing Company"
			self.existing_company = self.parent_company

	def set_default_accounts(self):
		self._set_default_account("default_cash_account", "Cash")
		self._set_default_account("default_bank_account", "Bank")
		self._set_default_account("round_off_account", "Round Off")
		self._set_default_account("accumulated_depreciation_account", "Accumulated Depreciation")
		self._set_default_account("depreciation_expense_account", "Depreciation")
		self._set_default_account("capital_work_in_progress_account", "Capital Work in Progress")
		self._set_default_account("asset_received_but_not_billed", "Asset Received But Not Billed")
		self._set_default_account("expenses_included_in_asset_valuation", "Expenses Included In Asset Valuation")

		if self.enable_perpetual_inventory:
			self._set_default_account("stock_received_but_not_billed", "Stock Received But Not Billed")
			self._set_default_account("default_inventory_account", "Stock")
			self._set_default_account("stock_adjustment_account", "Stock Adjustment")
			self._set_default_account("expenses_included_in_valuation", "Expenses Included In Valuation")
			self._set_default_account("default_expense_account", "Cost of Goods Sold")

		if not self.default_income_account:
			income_account = dataent.db.get_value("Account",
				{"account_name": _("Sales"), "company": self.name, "is_group": 0})

			if not income_account:
				income_account = dataent.db.get_value("Account",
					{"account_name": _("Sales Account"), "company": self.name})

			self.db_set("default_income_account", income_account)

		if not self.default_payable_account:
			self.db_set("default_payable_account", self.default_payable_account)

		if not self.default_payroll_payable_account:
			payroll_payable_account = dataent.db.get_value("Account",
				{"account_name": _("Payroll Payable"), "company": self.name, "is_group": 0})

			self.db_set("default_payroll_payable_account", payroll_payable_account)

		if not self.default_employee_advance_account:
			employe_advance_account = dataent.db.get_value("Account",
				{"account_name": _("Employee Advances"), "company": self.name, "is_group": 0})

			self.db_set("default_employee_advance_account", employe_advance_account)

		if not self.write_off_account:
			write_off_acct = dataent.db.get_value("Account",
				{"account_name": _("Write Off"), "company": self.name, "is_group": 0})

			self.db_set("write_off_account", write_off_acct)

		if not self.exchange_gain_loss_account:
			exchange_gain_loss_acct = dataent.db.get_value("Account",
				{"account_name": _("Exchange Gain/Loss"), "company": self.name, "is_group": 0})

			self.db_set("exchange_gain_loss_account", exchange_gain_loss_acct)

		if not self.disposal_account:
			disposal_acct = dataent.db.get_value("Account",
				{"account_name": _("Gain/Loss on Asset Disposal"), "company": self.name, "is_group": 0})

			self.db_set("disposal_account", disposal_acct)

	def _set_default_account(self, fieldname, account_type):
		if self.get(fieldname):
			return

		account = dataent.db.get_value("Account", {"account_type": account_type,
			"is_group": 0, "company": self.name})

		if account:
			self.db_set(fieldname, account)

	def set_mode_of_payment_account(self):
		cash = dataent.db.get_value('Mode of Payment', {'type': 'Cash'}, 'name')
		if cash and self.default_cash_account \
				and not dataent.db.get_value('Mode of Payment Account', {'company': self.name}):
			mode_of_payment = dataent.get_doc('Mode of Payment', cash)
			mode_of_payment.append('accounts', {
				'company': self.name,
				'default_account': self.default_cash_account
			})
			mode_of_payment.save(ignore_permissions=True)

	def create_default_cost_center(self):
		cc_list = [
			{
				'cost_center_name': self.name,
				'company':self.name,
				'is_group': 1,
				'parent_cost_center':None
			},
			{
				'cost_center_name':_('Main'),
				'company':self.name,
				'is_group':0,
				'parent_cost_center':self.name + ' - ' + self.abbr
			},
		]
		for cc in cc_list:
			cc.update({"doctype": "Cost Center"})
			cc_doc = dataent.get_doc(cc)
			cc_doc.flags.ignore_permissions = True

			if cc.get("cost_center_name") == self.name:
				cc_doc.flags.ignore_mandatory = True
			cc_doc.insert()

		dataent.db.set(self, "cost_center", _("Main") + " - " + self.abbr)
		dataent.db.set(self, "round_off_cost_center", _("Main") + " - " + self.abbr)
		dataent.db.set(self, "depreciation_cost_center", _("Main") + " - " + self.abbr)

	def after_rename(self, olddn, newdn, merge=False):
		dataent.db.set(self, "company_name", newdn)

		dataent.db.sql("""update `tabDefaultValue` set defvalue=%s
			where defkey='Company' and defvalue=%s""", (newdn, olddn))

		clear_defaults_cache()

	def abbreviate(self):
		self.abbr = ''.join([c[0].upper() for c in self.company_name.split()])

	def on_trash(self):
		"""
			Trash accounts and cost centers for this company if no gl entry exists
		"""
		NestedSet.validate_if_child_exists(self)
		dataent.utils.nestedset.update_nsm(self)

		rec = dataent.db.sql("SELECT name from `tabGL Entry` where company = %s", self.name)
		if not rec:
			dataent.db.sql("""delete from `tabBudget Account`
				where exists(select name from tabBudget
					where name=`tabBudget Account`.parent and company = %s)""", self.name)

			for doctype in ["Account", "Cost Center", "Budget", "Party Account"]:
				dataent.db.sql("delete from `tab{0}` where company = %s".format(doctype), self.name)

		if not dataent.db.get_value("Stock Ledger Entry", {"company": self.name}):
			dataent.db.sql("""delete from `tabWarehouse` where company=%s""", self.name)

		dataent.defaults.clear_default("company", value=self.name)
		for doctype in ["Mode of Payment Account", "Item Default"]:
			dataent.db.sql("delete from `tab{0}` where company = %s".format(doctype), self.name)

		# clear default accounts, warehouses from item
		warehouses = dataent.db.sql_list("select name from tabWarehouse where company=%s", self.name)
		if warehouses:
			dataent.db.sql("""delete from `tabItem Reorder` where warehouse in (%s)"""
				% ', '.join(['%s']*len(warehouses)), tuple(warehouses))

		# reset default company
		dataent.db.sql("""update `tabSingles` set value=""
			where doctype='Global Defaults' and field='default_company'
			and value=%s""", self.name)

		# delete BOMs
		boms = dataent.db.sql_list("select name from tabBOM where company=%s", self.name)
		if boms:
			dataent.db.sql("delete from tabBOM where company=%s", self.name)
			for dt in ("BOM Operation", "BOM Item", "BOM Scrap Item", "BOM Explosion Item"):
				dataent.db.sql("delete from `tab%s` where parent in (%s)"""
					% (dt, ', '.join(['%s']*len(boms))), tuple(boms))

		dataent.db.sql("delete from tabEmployee where company=%s", self.name)
		dataent.db.sql("delete from tabDepartment where company=%s", self.name)
		dataent.db.sql("delete from `tabTax Withholding Account` where company=%s", self.name)

		dataent.db.sql("delete from `tabSales Taxes and Charges Template` where company=%s", self.name)
		dataent.db.sql("delete from `tabPurchase Taxes and Charges Template` where company=%s", self.name)

@dataent.whitelist()
def enqueue_replace_abbr(company, old, new):
	kwargs = dict(company=company, old=old, new=new)
	dataent.enqueue('epaas.setup.doctype.company.company.replace_abbr', **kwargs)


@dataent.whitelist()
def replace_abbr(company, old, new):
	new = new.strip()
	if not new:
		dataent.throw(_("Abbr can not be blank or space"))

	dataent.only_for("System Manager")

	dataent.db.set_value("Company", company, "abbr", new)

	def _rename_record(doc):
		parts = doc[0].rsplit(" - ", 1)
		if len(parts) == 1 or parts[1].lower() == old.lower():
			dataent.rename_doc(dt, doc[0], parts[0] + " - " + new)

	def _rename_records(dt):
		# rename is expensive so let's be economical with memory usage
		doc = (d for d in dataent.db.sql("select name from `tab%s` where company=%s" % (dt, '%s'), company))
		for d in doc:
			_rename_record(d)

	for dt in ["Warehouse", "Account", "Cost Center", "Department",
			"Sales Taxes and Charges Template", "Purchase Taxes and Charges Template"]:
		_rename_records(dt)
		dataent.db.commit()


def get_name_with_abbr(name, company):
	company_abbr = dataent.get_cached_value('Company',  company,  "abbr")
	parts = name.split(" - ")

	if parts[-1].lower() != company_abbr.lower():
		parts.append(company_abbr)

	return " - ".join(parts)

def install_country_fixtures(company):
	company_doc = dataent.get_doc("Company", company)
	path = dataent.get_app_path('epaas', 'regional', dataent.scrub(company_doc.country))
	if os.path.exists(path.encode("utf-8")):
		dataent.get_attr("epaas.regional.{0}.setup.setup"
			.format(dataent.scrub(company_doc.country)))(company_doc, False)

def update_company_current_month_sales(company):
	current_month_year = formatdate(today(), "MM-yyyy")

	results = dataent.db.sql('''
		select
			sum(base_grand_total) as total, date_format(posting_date, '%m-%Y') as month_year
		from
			`tabSales Invoice`
		where
			date_format(posting_date, '%m-%Y')="{0}"
			and docstatus = 1
			and company = "{1}"
		group by
			month_year
	'''.format(current_month_year, dataent.db.escape(company)), as_dict = True)

	monthly_total = results[0]['total'] if len(results) > 0 else 0

	dataent.db.set_value("Company", company, "total_monthly_sales", monthly_total)

def update_company_monthly_sales(company):
	'''Cache past year monthly sales of every company based on sales invoices'''
	from dataent.utils.goal import get_monthly_results
	import json
	filter_str = "company = '{0}' and status != 'Draft' and docstatus=1".format(dataent.db.escape(company))
	month_to_value_dict = get_monthly_results("Sales Invoice", "base_grand_total",
		"posting_date", filter_str, "sum")

	dataent.db.set_value("Company", company, "sales_monthly_history", json.dumps(month_to_value_dict))

def update_transactions_annual_history(company, commit=False):
	transactions_history = get_all_transactions_annual_history(company)
	dataent.db.set_value("Company", company, "transactions_annual_history", json.dumps(transactions_history))

	if commit:
		dataent.db.commit()

def cache_companies_monthly_sales_history():
	companies = [d['name'] for d in dataent.get_list("Company")]
	for company in companies:
		update_company_monthly_sales(company)
		update_transactions_annual_history(company)
	dataent.db.commit()

@dataent.whitelist()
def get_children(doctype, parent=None, company=None, is_root=False):
	if parent == None or parent == "All Companies":
		parent = ""

	return dataent.db.sql("""
		select
			name as value,
			is_group as expandable
		from
			`tab{doctype}` comp
		where
			ifnull(parent_company, "")="{parent}"
		""".format(
			doctype = dataent.db.escape(doctype),
			parent=dataent.db.escape(parent)
		), as_dict=1)

@dataent.whitelist()
def add_node():
	from dataent.desk.treeview import make_tree_args
	args = dataent.form_dict
	args = make_tree_args(**args)

	if args.parent_company == 'All Companies':
		args.parent_company = None

	dataent.get_doc(args).insert()

def get_all_transactions_annual_history(company):
	out = {}

	items = dataent.db.sql('''
		select transaction_date, count(*) as count

		from (
			select name, transaction_date, company
			from `tabQuotation`

			UNION ALL

			select name, transaction_date, company
			from `tabSales Order`

			UNION ALL

			select name, posting_date as transaction_date, company
			from `tabDelivery Note`

			UNION ALL

			select name, posting_date as transaction_date, company
			from `tabSales Invoice`

			UNION ALL

			select name, creation as transaction_date, company
			from `tabIssue`

			UNION ALL

			select name, creation as transaction_date, company
			from `tabProject`
		) t

		where
			company=%s
			and
			transaction_date > date_sub(curdate(), interval 1 year)

		group by
			transaction_date
			''', (company), as_dict=True)

	for d in items:
		timestamp = get_timestamp(d["transaction_date"])
		out.update({ timestamp: d["count"] })

	return out

def get_timeline_data(doctype, name):
	'''returns timeline data based on linked records in dashboard'''
	out = {}
	date_to_value_dict = {}

	history = dataent.get_cached_value('Company',  name,  "transactions_annual_history")

	try:
		date_to_value_dict = json.loads(history) if history and '{' in history else None
	except ValueError:
		date_to_value_dict = None

	if date_to_value_dict is None:
		update_transactions_annual_history(name, True)
		history = dataent.get_cached_value('Company',  name,  "transactions_annual_history")
		return json.loads(history) if history and '{' in history else {}

	return date_to_value_dict
