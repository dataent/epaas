from __future__ import unicode_literals
import dataent
from pymysql import InternalError

def execute():
	dataent.reload_doctype("Journal Entry Account")
	for doctype, fieldname in (
		("Sales Order", "against_sales_order"),
		("Purchase Order", "against_purchase_order"),
		("Sales Invoice", "against_invoice"),
		("Purchase Invoice", "against_voucher"),
		("Journal Entry", "against_jv"),
		("Expense Claim", "against_expense_claim"),
	):
		try:
			dataent.db.sql("""update `tabJournal Entry Account`
				set reference_type=%s, reference_name={0} where ifnull({0}, '') != ''
			""".format(fieldname), doctype)
		except InternalError:
			# column not found
			pass
