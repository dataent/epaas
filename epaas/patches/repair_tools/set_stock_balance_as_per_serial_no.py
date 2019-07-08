# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

def execute():
	from epaas.stock.stock_balance import set_stock_balance_as_per_serial_no
	dataent.db.auto_commit_on_many_writes = 1

	set_stock_balance_as_per_serial_no()

	dataent.db.auto_commit_on_many_writes = 0
