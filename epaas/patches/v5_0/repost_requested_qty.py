# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

def execute():
	from epaas.stock.stock_balance import update_bin_qty, get_indented_qty

	count=0
	for item_code, warehouse in dataent.db.sql("""select distinct item_code, warehouse 
		from `tabMaterial Request Item` where docstatus = 1"""):
			try:
				count += 1
				update_bin_qty(item_code, warehouse, {
					"indented_qty": get_indented_qty(item_code, warehouse),
				})
				if count % 200 == 0:
					dataent.db.commit()
			except:
				dataent.db.rollback()
