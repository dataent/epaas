# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent


from dataent.utils import flt
from dataent import _

from dataent.utils.nestedset import NestedSet

class Territory(NestedSet):
	nsm_parent_field = 'parent_territory'

	def validate(self):
		for d in self.get('targets') or []:
			if not flt(d.target_qty) and not flt(d.target_amount):
				dataent.throw(_("Either target qty or target amount is mandatory"))

	def on_update(self):
		super(Territory, self).on_update()
		self.validate_one_root()

def on_doctype_update():
	dataent.db.add_index("Territory", ["lft", "rgt"])