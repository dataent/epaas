# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent
from dataent import _
from dataent.utils import flt
from dataent.utils.nestedset import NestedSet
from epaas import get_default_currency

class SalesPerson(NestedSet):
	nsm_parent_field = 'parent_sales_person'

	def validate(self):
		for d in self.get('targets') or []:
			if not flt(d.target_qty) and not flt(d.target_amount):
				dataent.throw(_("Either target qty or target amount is mandatory."))
		self.validate_employee_id()

	def onload(self):
		self.load_dashboard_info()

	def load_dashboard_info(self):
		company_default_currency = get_default_currency()

		allocated_amount = dataent.db.sql("""
			select sum(allocated_amount)
			from `tabSales Team`
			where sales_person = %s and docstatus=1 and parenttype = 'Sales Order'
		""",(self.sales_person_name))

		info = {}
		info["allocated_amount"] = flt(allocated_amount[0][0]) if allocated_amount else 0
		info["currency"] = company_default_currency

		self.set_onload('dashboard_info', info)

	def on_update(self):
		super(SalesPerson, self).on_update()
		self.validate_one_root()

	def get_email_id(self):
		if self.employee:
			user = dataent.db.get_value("Employee", self.employee, "user_id")
			if not user:
				dataent.throw(_("User ID not set for Employee {0}").format(self.employee))
			else:
				return dataent.db.get_value("User", user, "email") or user

	def validate_employee_id(self):
		if self.employee:
			sales_person = dataent.db.get_value("Sales Person", {"employee": self.employee})

			if sales_person and sales_person != self.name:
				dataent.throw(_("Another Sales Person {0} exists with the same Employee id").format(sales_person))

def on_doctype_update():
	dataent.db.add_index("Sales Person", ["lft", "rgt"])

def get_timeline_data(doctype, name):

	out = {}

	out.update(dict(dataent.db.sql('''select
			unix_timestamp(dt.transaction_date), count(st.parenttype)
		from
			`tabSales Order` dt, `tabSales Team` st
		where
			st.sales_person = %s and st.parent = dt.name and dt.transaction_date > date_sub(curdate(), interval 1 year)
			group by dt.transaction_date ''', name)))

	sales_invoice = dict(dataent.db.sql('''select
			unix_timestamp(dt.posting_date), count(st.parenttype)
		from
			`tabSales Invoice` dt, `tabSales Team` st
		where
			st.sales_person = %s and st.parent = dt.name and dt.posting_date > date_sub(curdate(), interval 1 year)
			group by dt.posting_date ''', name))

	for key in sales_invoice:
		if out.get(key):
			out[key] += sales_invoice[key]
		else:
			out[key] = sales_invoice[key]

	delivery_note = dict(dataent.db.sql('''select
			unix_timestamp(dt.posting_date), count(st.parenttype)
		from
			`tabDelivery Note` dt, `tabSales Team` st
		where
			st.sales_person = %s and st.parent = dt.name and dt.posting_date > date_sub(curdate(), interval 1 year)
			group by dt.posting_date ''', name))

	for key in delivery_note:
		if out.get(key):
			out[key] += delivery_note[key]
		else:
			out[key] = delivery_note[key]

	return out
