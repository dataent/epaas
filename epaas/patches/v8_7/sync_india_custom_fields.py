from __future__ import unicode_literals
import dataent
from epaas.regional.india.setup  import make_custom_fields

def execute():
	company = dataent.get_all('Company', filters = {'country': 'India'})
	if not company:
		return

	dataent.reload_doc('hr', 'doctype', 'payroll_period')
	dataent.reload_doc('hr', 'doctype', 'employee_tax_exemption_declaration')
	dataent.reload_doc('hr', 'doctype', 'employee_tax_exemption_proof_submission')
	dataent.reload_doc('hr', 'doctype', 'employee_tax_exemption_declaration_category')
	dataent.reload_doc('hr', 'doctype', 'employee_tax_exemption_proof_submission_detail')

	for doctype in ["Sales Invoice", "Delivery Note", "Purchase Invoice"]:
		dataent.db.sql("""delete from `tabCustom Field` where dt = %s
			and fieldname in ('port_code', 'shipping_bill_number', 'shipping_bill_date')""", doctype)

	make_custom_fields()

	dataent.db.sql("""
		update `tabCustom Field`
		set reqd = 0, `default` = ''
		where fieldname = 'reason_for_issuing_document'
	""")

	dataent.db.sql("""
		update tabAddress
		set gst_state_number=concat("0", gst_state_number)
		where ifnull(gst_state_number, '') != '' and gst_state_number<10
	""")