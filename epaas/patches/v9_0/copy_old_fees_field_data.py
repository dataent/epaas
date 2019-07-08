# Copyright (c) 2017, Dataent and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

def execute():
	# 'Schools' module changed to the 'Education'
	# dataent.reload_doc("schools", "doctype", "fees")
	dataent.reload_doc("education", "doctype", "fees")

	if "total_amount" not in dataent.db.get_table_columns("Fees"):
		return

	dataent.db.sql("""update tabFees set grand_total=total_amount where grand_total = 0.0""")