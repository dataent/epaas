# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import print_function, unicode_literals
import dataent, epaas

def execute():
	dataent.reload_doctype("Account")

	warehouses = dataent.db.sql("""select name, company from tabAccount
		where account_type = 'Stock' and is_group = 0
		and (warehouse is null or warehouse = '')""", as_dict=1)
	warehouses = [d.name for d in warehouses if epaas.is_perpetual_inventory_enabled(d.company)]

	if len(warehouses) > 0:
		warehouses = set_warehouse_for_stock_account(warehouses)
		if not warehouses:
			return

		stock_vouchers = dataent.db.sql("""select distinct sle.voucher_type, sle.voucher_no
			from `tabStock Ledger Entry` sle
			where sle.warehouse in (%s) and creation > '2016-05-01'
			and not exists(select name from `tabGL Entry` 
				where account=sle.warehouse and voucher_type=sle.voucher_type and voucher_no=sle.voucher_no)
			order by sle.posting_date""" %
			', '.join(['%s']*len(warehouses)), tuple(warehouses))

		rejected = []
		for voucher_type, voucher_no in stock_vouchers:
			try:
				dataent.db.sql("""delete from `tabGL Entry`
					where voucher_type=%s and voucher_no=%s""", (voucher_type, voucher_no))

				voucher = dataent.get_doc(voucher_type, voucher_no)
				voucher.make_gl_entries()
				dataent.db.commit()
			except Exception as e:
				print(dataent.get_traceback())
				rejected.append([voucher_type, voucher_no])
				dataent.db.rollback()

		print(rejected)

def set_warehouse_for_stock_account(warehouse_account):
	for account in warehouse_account:
		if dataent.db.exists('Warehouse', account):
			dataent.db.set_value("Account", account, "warehouse", account)
		else:
			warehouse_account.remove(account)

	return warehouse_account
