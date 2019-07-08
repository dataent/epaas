# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent
import json

def execute():
	existing_allow_negative_stock = dataent.db.get_value("Stock Settings", None, "allow_negative_stock")
	dataent.db.set_value("Stock Settings", None, "allow_negative_stock", 1)

	head_row = ["Item Code", "Warehouse", "Quantity", "Valuation Rate"]
	stock_reco_to_be_reposted = []
	for d in dataent.db.sql("""select name, reconciliation_json from `tabStock Reconciliation`
		where docstatus=1 and creation > '2014-03-01'""", as_dict=1):
			data = json.loads(d.reconciliation_json)
			for row in data[data.index(head_row)+1:]:
				if row[3] in ["", None]:
					stock_reco_to_be_reposted.append(d.name)
					break

	for dn in stock_reco_to_be_reposted:
		reco = dataent.get_doc("Stock Reconciliation", dn)
		reco.docstatus = 2
		reco.on_cancel()

		reco.docstatus = 1
		reco.validate()
		reco.on_submit()

	dataent.db.set_value("Stock Settings", None, "allow_negative_stock", existing_allow_negative_stock)
