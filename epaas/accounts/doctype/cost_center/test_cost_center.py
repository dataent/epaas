# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt
from __future__ import unicode_literals


import dataent
test_records = dataent.get_test_records('Cost Center')



def create_cost_center(**args):
	args = dataent._dict(args)
	if args.cost_center_name:
		company = args.company or "_Test Company"
		company_abbr = dataent.db.get_value("Company", company, "abbr")
		cc_name = args.cost_center_name + " - " + company_abbr
		if not dataent.db.exists("Cost Center", cc_name):
			cc = dataent.new_doc("Cost Center")
			cc.company = args.company or "_Test Company"
			cc.cost_center_name = args.cost_center_name
			cc.is_group = args.is_group or 0
			cc.parent_cost_center = args.parent_cost_center or "_Test Company - _TC"
			cc.insert()



