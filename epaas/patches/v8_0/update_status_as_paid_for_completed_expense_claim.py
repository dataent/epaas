# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

def execute():
	""" set status as Paid in Expense Claim if total_sactioned_amount 
		and total_amount_reimbursed is equal """
	
	dataent.reload_doctype('Expense Claim')

	dataent.db.sql("""
		update 
			`tabExpense Claim`
		set status = 'Paid'
		where 
			total_sanctioned_amount = total_amount_reimbursed
	""")
