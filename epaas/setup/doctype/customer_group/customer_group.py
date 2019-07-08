# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent
from dataent import _


from dataent.utils.nestedset import NestedSet
class CustomerGroup(NestedSet):
	nsm_parent_field = 'parent_customer_group';

	def on_update(self):
		self.validate_name_with_customer()
		super(CustomerGroup, self).on_update()
		self.validate_one_root()

	def validate_name_with_customer(self):
		if dataent.db.exists("Customer", self.name):
			dataent.msgprint(_("A customer with the same name already exists"), raise_exception=1)

def get_parent_customer_groups(customer_group):
	lft, rgt = dataent.db.get_value("Customer Group", customer_group, ['lft', 'rgt'])

	return dataent.db.sql("""select name from `tabCustomer Group`
		where lft <= %s and rgt >= %s
		order by lft asc""", (lft, rgt), as_dict=True)

def on_doctype_update():
	dataent.db.add_index("Customer Group", ["lft", "rgt"])