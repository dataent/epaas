from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doc('accounts', 'doctype', 'sales_invoice_timesheet')
	dataent.reload_doc('accounts', 'doctype', 'sales_invoice_payment')
	dataent.reload_doc('accounts', 'doctype', 'mode_of_payment')

	count = 0
	for data in dataent.db.sql("""select name, mode_of_payment, cash_bank_account, paid_amount, company 
		from `tabSales Invoice` si
		where si.is_pos = 1 and si.docstatus < 2 
		and si.cash_bank_account is not null and si.cash_bank_account != ''
		and not exists(select name from `tabSales Invoice Payment` where parent=si.name)""", as_dict=1):
		
		if not data.mode_of_payment and not dataent.db.exists("Mode of Payment", "Cash"):
			mop = dataent.new_doc("Mode of Payment")
			mop.mode_of_payment = "Cash"
			mop.type = "Cash"
			mop.save()
		
		si_doc = dataent.get_doc('Sales Invoice', data.name)
		row = si_doc.append('payments', {
			'mode_of_payment': data.mode_of_payment or 'Cash',
			'account': data.cash_bank_account,
			'type': dataent.db.get_value('Mode of Payment', data.mode_of_payment, 'type') or 'Cash',
			'amount': data.paid_amount
		})
		row.db_update()
		
		si_doc.set_paid_amount()
		si_doc.db_set("paid_amount", si_doc.paid_amount, update_modified = False)
		si_doc.db_set("base_paid_amount", si_doc.base_paid_amount, update_modified = False)
		
		count +=1
		
		if count % 200 == 0:
			dataent.db.commit()