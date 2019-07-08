from __future__ import unicode_literals
import dataent

from epaas.accounts.doctype.budget.budget import DuplicateBudgetError

def execute():
	dataent.reload_doc("accounts", "doctype", "budget")
	dataent.reload_doc("accounts", "doctype", "budget_account")

	existing_budgets = dataent.db.sql("""
		select
			cc.name, cc.company, cc.distribution_id,
			budget.account, budget.budget_allocated, budget.fiscal_year
		from
			`tabCost Center` cc, `tabBudget Detail` budget
		where
			cc.name=budget.parent
	""", as_dict=1)

	actions = {}
	for d in dataent.db.sql("select name, yearly_bgt_flag, monthly_bgt_flag from tabCompany", as_dict=1):
		actions.setdefault(d.name, d)

	budget_records = []
	for d in existing_budgets:
		budget = dataent.db.get_value("Budget",
			{"cost_center": d.name, "fiscal_year": d.fiscal_year, "company": d.company})

		if not budget:
			budget = dataent.new_doc("Budget")
			budget.cost_center = d.name
			budget.fiscal_year = d.fiscal_year
			budget.monthly_distribution = d.distribution_id
			budget.company = d.company
			if actions[d.company]["yearly_bgt_flag"]:
				budget.action_if_annual_budget_exceeded = actions[d.company]["yearly_bgt_flag"]
			if actions[d.company]["monthly_bgt_flag"]:
				budget.action_if_accumulated_monthly_budget_exceeded = actions[d.company]["monthly_bgt_flag"]
		else:
			budget = dataent.get_doc("Budget", budget)

		budget.append("accounts", {
			"account": d.account,
			"budget_amount": d.budget_allocated
		})

		try:
			budget.insert()
			budget_records.append(budget)
		except DuplicateBudgetError:
			pass

	for budget in budget_records:
		budget.submit()

	if dataent.db.get_value("DocType", "Budget Detail"):
		dataent.delete_doc("DocType", "Budget Detail")