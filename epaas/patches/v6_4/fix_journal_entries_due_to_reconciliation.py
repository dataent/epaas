# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import print_function, unicode_literals
import dataent

def execute():
	dataent.reload_doctype("Sales Invoice Advance")
	dataent.reload_doctype("Purchase Invoice Advance")
	
	je_rows = dataent.db.sql("""
		select name, parent, reference_type, reference_name, debit, credit
		from `tabJournal Entry Account`
		where docstatus=1 and date(modified) >= '2015-09-17'
			and ((ifnull(debit_in_account_currency, 0)*exchange_rate != ifnull(debit, 0))
			or (ifnull(credit_in_account_currency, 0)*exchange_rate != ifnull(credit, 0)))
		order by parent
	""", as_dict=True)

	journal_entries = []
	
	for d in je_rows:
		if d.parent not in journal_entries:
			journal_entries.append(d.parent)

		is_advance_entry=None
		if d.reference_type in ("Sales Invoice", "Purchase Invoice") and d.reference_name:
			is_advance_entry = dataent.db.sql("""select name from `tab{0}` 
				where reference_name=%s and reference_row=%s 
					and ifnull(allocated_amount, 0) > 0 and docstatus=1"""
				.format(d.reference_type + " Advance"), (d.parent, d.name))
				
		if is_advance_entry or not (d.debit or d.credit):
			dataent.db.sql("""
				update `tabJournal Entry Account`
				set	debit=debit_in_account_currency*exchange_rate,
					credit=credit_in_account_currency*exchange_rate
				where name=%s""", d.name)
		else:
			dataent.db.sql("""
				update `tabJournal Entry Account`
				set debit_in_account_currency=debit/exchange_rate,
					credit_in_account_currency=credit/exchange_rate
				where name=%s""", d.name)

	for d in journal_entries:
		print(d)
		# delete existing gle
		dataent.db.sql("delete from `tabGL Entry` where voucher_type='Journal Entry' and voucher_no=%s", d)

		# repost gl entries
		je = dataent.get_doc("Journal Entry", d)
		je.make_gl_entries()