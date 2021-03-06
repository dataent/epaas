 # -*- coding: utf-8 -*-
# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import dataent
from dataent import _
from dataent.utils import flt, getdate, add_months, get_last_day, fmt_money, nowdate
from dataent.model.naming import make_autoname
from epaas.accounts.utils import get_fiscal_year
from dataent.model.document import Document

class BudgetError(dataent.ValidationError): pass
class DuplicateBudgetError(dataent.ValidationError): pass

class Budget(Document):
	def autoname(self):
		self.name = make_autoname(self.get(dataent.scrub(self.budget_against)) 
			+ "/" + self.fiscal_year + "/.###")

	def validate(self):
		if not self.get(dataent.scrub(self.budget_against)):
			dataent.throw(_("{0} is mandatory").format(self.budget_against))
		self.validate_duplicate()
		self.validate_accounts()
		self.set_null_value()
		self.validate_applicable_for()

	def validate_duplicate(self):
		budget_against_field = dataent.scrub(self.budget_against)
		budget_against = self.get(budget_against_field)

		accounts = [d.account for d in self.accounts] or []
		existing_budget = dataent.db.sql("""
			select
				b.name, ba.account from `tabBudget` b, `tabBudget Account` ba
			where
				ba.parent = b.name and b.docstatus < 2 and b.company = %s and %s=%s and
				b.fiscal_year=%s and b.name != %s and ba.account in (%s) """
				% ('%s', budget_against_field, '%s', '%s', '%s', ','.join(['%s'] * len(accounts))),
			(self.company, budget_against, self.fiscal_year, self.name) + tuple(accounts), as_dict=1)

		for d in existing_budget:
			dataent.throw(_("Another Budget record '{0}' already exists against {1} '{2}' and account '{3}' for fiscal year {4}")
				.format(d.name, self.budget_against, budget_against, d.account, self.fiscal_year), DuplicateBudgetError)

	def validate_accounts(self):
		account_list = []
		for d in self.get('accounts'):
			if d.account:
				account_details = dataent.db.get_value("Account", d.account,
					["is_group", "company", "report_type"], as_dict=1)

				if account_details.is_group:
					dataent.throw(_("Budget cannot be assigned against Group Account {0}").format(d.account))
				elif account_details.company != self.company:
					dataent.throw(_("Account {0} does not belongs to company {1}")
						.format(d.account, self.company))
				elif account_details.report_type != "Profit and Loss":
					dataent.throw(_("Budget cannot be assigned against {0}, as it's not an Income or Expense account")
						.format(d.account))

				if d.account in account_list:
					dataent.throw(_("Account {0} has been entered multiple times").format(d.account))
				else:
					account_list.append(d.account)

	def set_null_value(self):
		if self.budget_against == 'Cost Center':
			self.project = None
		else:
			self.cost_center = None

	def validate_applicable_for(self):
		if (self.applicable_on_material_request
			and not (self.applicable_on_purchase_order and self.applicable_on_booking_actual_expenses)):
			dataent.throw(_("Please enable Applicable on Purchase Order and Applicable on Booking Actual Expenses"))

		elif (self.applicable_on_purchase_order
			and not (self.applicable_on_booking_actual_expenses)):
			dataent.throw(_("Please enable Applicable on Booking Actual Expenses"))

		elif not(self.applicable_on_material_request
			or self.applicable_on_purchase_order or self.applicable_on_booking_actual_expenses):
			self.applicable_on_booking_actual_expenses = 1

def validate_expense_against_budget(args):
	args = dataent._dict(args)

	if args.get('company') and not args.fiscal_year:
		args.fiscal_year = get_fiscal_year(args.get('posting_date'), company=args.get('company'))[0]
		dataent.flags.exception_approver_role = dataent.get_cached_value('Company', 
			args.get('company'),  'exception_budget_approver_role')

	if not args.account:
		args.account = args.get("expense_account")

	if not (args.get('account') and args.get('cost_center')) and args.item_code:
		args.cost_center, args.account = get_item_details(args)

	if not (args.cost_center or args.project) and not args.account:
		return

	for budget_against in ['project', 'cost_center']:
		if (args.get(budget_against) and args.account
				and dataent.db.get_value("Account", {"name": args.account, "root_type": "Expense"})):

			if args.project and budget_against == 'project':
				condition = "and b.project='%s'" % dataent.db.escape(args.project)
				args.budget_against_field = "Project"
			
			elif args.cost_center and budget_against == 'cost_center':
				cc_lft, cc_rgt = dataent.db.get_value("Cost Center", args.cost_center, ["lft", "rgt"])
				condition = """and exists(select name from `tabCost Center` 
					where lft<=%s and rgt>=%s and name=b.cost_center)""" % (cc_lft, cc_rgt)
				args.budget_against_field = "Cost Center"

			args.budget_against = args.get(budget_against)

			budget_records = dataent.db.sql("""
				select
					b.{budget_against_field} as budget_against, ba.budget_amount, b.monthly_distribution,
					ifnull(b.applicable_on_material_request, 0) as for_material_request,
					ifnull(applicable_on_purchase_order,0) as for_purchase_order,
					ifnull(applicable_on_booking_actual_expenses,0) as for_actual_expenses,
					b.action_if_annual_budget_exceeded, b.action_if_accumulated_monthly_budget_exceeded,
					b.action_if_annual_budget_exceeded_on_mr, b.action_if_accumulated_monthly_budget_exceeded_on_mr,
					b.action_if_annual_budget_exceeded_on_po, b.action_if_accumulated_monthly_budget_exceeded_on_po
				from 
					`tabBudget` b, `tabBudget Account` ba
				where
					b.name=ba.parent and b.fiscal_year=%s 
					and ba.account=%s and b.docstatus=1
					{condition}
			""".format(condition=condition, 
				budget_against_field=dataent.scrub(args.get("budget_against_field"))),
				(args.fiscal_year, args.account), as_dict=True)

			if budget_records:
				validate_budget_records(args, budget_records)

def validate_budget_records(args, budget_records):
	for budget in budget_records:
		if flt(budget.budget_amount):
			amount = get_amount(args, budget)
			yearly_action, monthly_action = get_actions(args, budget)

			if monthly_action in ["Stop", "Warn"]:
				budget_amount = get_accumulated_monthly_budget(budget.monthly_distribution,
					args.posting_date, args.fiscal_year, budget.budget_amount)

				args["month_end_date"] = get_last_day(args.posting_date)

				compare_expense_with_budget(args, budget_amount, 
					_("Accumulated Monthly"), monthly_action, budget.budget_against, amount)

			if yearly_action in ("Stop", "Warn") and monthly_action != "Stop" \
				and yearly_action != monthly_action:
				compare_expense_with_budget(args, flt(budget.budget_amount), 
						_("Annual"), yearly_action, budget.budget_against, amount)

def compare_expense_with_budget(args, budget_amount, action_for, action, budget_against, amount=0):
	actual_expense = amount or get_actual_expense(args)
	if actual_expense > budget_amount:
		diff = actual_expense - budget_amount
		currency = dataent.get_cached_value('Company',  args.company,  'default_currency')

		msg = _("{0} Budget for Account {1} against {2} {3} is {4}. It will exceed by {5}").format(
				_(action_for), dataent.bold(args.account), args.budget_against_field, 
				dataent.bold(budget_against),
				dataent.bold(fmt_money(budget_amount, currency=currency)), 
				dataent.bold(fmt_money(diff, currency=currency)))

		if (dataent.flags.exception_approver_role
			and dataent.flags.exception_approver_role in dataent.get_roles(dataent.session.user)):
			action = "Warn"

		if action=="Stop":
			dataent.throw(msg, BudgetError)
		else:
			dataent.msgprint(msg, indicator='orange')

def get_actions(args, budget):
	yearly_action = budget.action_if_annual_budget_exceeded
	monthly_action = budget.action_if_accumulated_monthly_budget_exceeded

	if args.get('doctype') == 'Material Request' and budget.for_material_request:
		yearly_action = budget.action_if_annual_budget_exceeded_on_mr
		monthly_action = budget.action_if_accumulated_monthly_budget_exceeded_on_mr

	elif args.get('doctype') == 'Purchase Order' and budget.for_purchase_order:
		yearly_action = budget.action_if_annual_budget_exceeded_on_po
		monthly_action = budget.action_if_accumulated_monthly_budget_exceeded_on_po

	return yearly_action, monthly_action

def get_amount(args, budget):
	amount = 0

	if args.get('doctype') == 'Material Request' and budget.for_material_request:
		amount = (get_requested_amount(args, budget)
			+ get_ordered_amount(args, budget) + get_actual_expense(args))

	elif args.get('doctype') == 'Purchase Order' and budget.for_purchase_order:
		amount = get_ordered_amount(args, budget) + get_actual_expense(args)

	return amount

def get_requested_amount(args, budget):
	item_code = args.get('item_code')
	condition = get_other_condition(args, budget, 'Material Request')

	data = dataent.db.sql(""" select ifnull((sum(mri.stock_qty - mri.ordered_qty) * rate), 0) as amount
		from `tabMaterial Request Item` mri, `tabMaterial Request` mr where mr.name = mri.parent and
		mri.item_code = %s and mr.docstatus = 1 and mri.stock_qty > mri.ordered_qty and {0} and
		mr.material_request_type = 'Purchase' and mr.status != 'Stopped'""".format(condition), item_code, as_list=1)

	return data[0][0] if data else 0

def get_ordered_amount(args, budget):
	item_code = args.get('item_code')
	condition = get_other_condition(args, budget, 'Purchase Order')

	data = dataent.db.sql(""" select ifnull(sum(poi.amount - poi.billed_amt), 0) as amount
		from `tabPurchase Order Item` poi, `tabPurchase Order` po where
		po.name = poi.parent and poi.item_code = %s and po.docstatus = 1 and poi.amount > poi.billed_amt
		and po.status != 'Closed' and {0}""".format(condition), item_code, as_list=1)

	return data[0][0] if data else 0

def get_other_condition(args, budget, for_doc):
	condition = "expense_account = '%s'" % (args.expense_account)
	budget_against_field = dataent.scrub(args.get("budget_against_field"))

	if budget_against_field and args.get(budget_against_field):
		condition += " and %s = '%s'" %(budget_against_field, args.get(budget_against_field))

	if args.get('fiscal_year'):
		date_field = 'schedule_date' if for_doc == 'Material Request' else 'transaction_date'
		start_date, end_date = dataent.db.get_value('Fiscal Year', args.get('fiscal_year'),
			['year_start_date', 'year_end_date'])

		alias = 'mr' if for_doc == 'Material Request' else 'po'
		condition += """ and %s.%s
			between '%s' and '%s' """ %(alias, date_field, start_date, end_date)

	return condition

def get_actual_expense(args):
	condition1 = " and gle.posting_date <= %(month_end_date)s" \
		if args.get("month_end_date") else ""
	if args.budget_against_field == "Cost Center":
		lft_rgt = dataent.db.get_value(args.budget_against_field, 
			args.budget_against, ["lft", "rgt"], as_dict=1)
		args.update(lft_rgt)
		condition2 = """and exists(select name from `tabCost Center` 
			where lft>=%(lft)s and rgt<=%(rgt)s and name=gle.cost_center)"""
	
	elif args.budget_against_field == "Project":
		condition2 = "and exists(select name from `tabProject` where name=gle.project and gle.project = %(budget_against)s)"

	return flt(dataent.db.sql("""
		select sum(gle.debit) - sum(gle.credit)
		from `tabGL Entry` gle
		where gle.account=%(account)s
			{condition1}
			and gle.fiscal_year=%(fiscal_year)s
			and gle.company=%(company)s
			and gle.docstatus=1
			{condition2}
	""".format(condition1=condition1, condition2=condition2), (args))[0][0])

def get_accumulated_monthly_budget(monthly_distribution, posting_date, fiscal_year, annual_budget):
	distribution = {}
	if monthly_distribution:
		for d in dataent.db.sql("""select mdp.month, mdp.percentage_allocation
			from `tabMonthly Distribution Percentage` mdp, `tabMonthly Distribution` md
			where mdp.parent=md.name and md.fiscal_year=%s""", fiscal_year, as_dict=1):
				distribution.setdefault(d.month, d.percentage_allocation)

	dt = dataent.db.get_value("Fiscal Year", fiscal_year, "year_start_date")
	accumulated_percentage = 0.0

	while(dt <= getdate(posting_date)):
		if monthly_distribution:
			accumulated_percentage += distribution.get(getdate(dt).strftime("%B"), 0)
		else:
			accumulated_percentage += 100.0/12

		dt = add_months(dt, 1)

	return annual_budget * accumulated_percentage / 100

def get_item_details(args):
	cost_center, expense_account = None, None

	if not args.get('company'):
		return cost_center, expense_account

	if args.item_code:
		item_defaults = dataent.db.get_value('Item Default',
			{'parent': args.item_code, 'company': args.get('company')},
			['buying_cost_center', 'expense_account'])
		if item_defaults:
			cost_center, expense_account = item_defaults

	if not (cost_center and expense_account):
		for doctype in ['Item Group', 'Company']:
			data = get_expense_cost_center(doctype, args)

			if not cost_center and data:
				cost_center = data[0]

			if not expense_account and data:
				expense_account = data[1]

			if cost_center and expense_account:
				return cost_center, expense_account

	return cost_center, expense_account

def get_expense_cost_center(doctype, args):
	if doctype == 'Item Group':
		return dataent.db.get_value('Item Default',
			{'parent': args.get(dataent.scrub(doctype)), 'company': args.get('company')},
			['buying_cost_center', 'expense_account'])
	else:
		return dataent.db.get_value(doctype, args.get(dataent.scrub(doctype)),\
			['cost_center', 'default_expense_account'])
