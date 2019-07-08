# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

def execute():
	# update the selling settings and set the close_opportunity_after_days
	dataent.reload_doc("selling", "doctype", "selling_settings")
	dataent.db.set_value("Selling Settings", "Selling Settings", "close_opportunity_after_days", 15)

	# Auto close Replied opportunity
	dataent.db.sql("""update `tabOpportunity` set status='Closed' where status='Replied'
		 and date_sub(curdate(), interval 15 Day)>modified""")

	# create Support Settings doctype and update close_issue_after_days
	dataent.reload_doc("support", "doctype", "support_settings")
	dataent.db.set_value("Support Settings", "Support Settings", "close_issue_after_days", 7)