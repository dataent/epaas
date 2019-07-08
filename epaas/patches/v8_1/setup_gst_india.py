from __future__ import unicode_literals
import dataent
from dataent.email import sendmail_to_system_managers

def execute():
	dataent.reload_doc('stock', 'doctype', 'item')
	dataent.reload_doc("stock", "doctype", "customs_tariff_number")
	dataent.reload_doc("accounts", "doctype", "payment_terms_template")
	dataent.reload_doc("accounts", "doctype", "payment_schedule")

	company = dataent.get_all('Company', filters = {'country': 'India'})
	if not company:
		return

	dataent.reload_doc('regional', 'doctype', 'gst_settings')
	dataent.reload_doc('regional', 'doctype', 'gst_hsn_code')

	for report_name in ('GST Sales Register', 'GST Purchase Register',
		'GST Itemised Sales Register', 'GST Itemised Purchase Register'):

		dataent.reload_doc('regional', 'report', dataent.scrub(report_name))

	from epaas.regional.india.setup import setup
	delete_custom_field_tax_id_if_exists()
	setup(patch=True)
	send_gst_update_email()

def delete_custom_field_tax_id_if_exists():
	for field in dataent.db.sql_list("""select name from `tabCustom Field` where fieldname='tax_id'
		and dt in ('Sales Order', 'Sales Invoice', 'Delivery Note')"""):
		dataent.delete_doc("Custom Field", field, ignore_permissions=True)
		dataent.db.commit()

def send_gst_update_email():
	message = """Hello,

<p>EPAAS is now GST Ready!</p>

<p>To start making GST Invoices from 1st of July, you just need to create new Tax Accounts,
Templates and update your Customer's and Supplier's GST Numbers.</p>

<p>Please refer {gst_document_link} to know more about how to setup and implement GST in EPAAS.</p>

<p>Please contact us at support@epaas.xyz, if you have any questions.</p>

<p>Thanks,</p>
EPAAS Team.
	""".format(gst_document_link="<a href='http://dataent.github.io/epaas/user/manual/en/regional/india/'> EPAAS GST Document </a>")

	try:
		sendmail_to_system_managers("[Important] EPAAS GST updates", message)
	except Exception as e:
		pass