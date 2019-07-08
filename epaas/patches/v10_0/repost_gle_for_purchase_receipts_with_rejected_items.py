# Copyright (c) 2017, Dataent and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent, epaas

def execute():
	for company in dataent.get_all("Company"):
		if not epaas.is_perpetual_inventory_enabled(company.name):
			continue

		acc_frozen_upto = dataent.db.get_value("Accounts Settings", None, "acc_frozen_upto") or "1900-01-01"
		pr_with_rejected_warehouse = dataent.db.sql("""
			select pr.name
			from `tabPurchase Receipt` pr, `tabPurchase Receipt Item` pr_item
			where pr.name = pr_item.parent
				and pr.posting_date > %s
				and pr.docstatus=1
				and pr.company = %s
				and pr_item.rejected_qty > 0
		""", (acc_frozen_upto, company.name), as_dict=1)

		for d in pr_with_rejected_warehouse:
			doc = dataent.get_doc("Purchase Receipt", d.name)

			doc.docstatus = 2
			doc.make_gl_entries_on_cancel(repost_future_gle=False)


			# update gl entries for submit state of PR
			doc.docstatus = 1
			doc.make_gl_entries(repost_future_gle=False)
