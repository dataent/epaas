# Copyright (c) 2018, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt
from __future__ import unicode_literals
import dataent
from dataent import _
from epaas.epaas_integrations.doctype.gocardless_settings.gocardless_settings import gocardless_initialization, get_gateway_controller

no_cache = 1
no_sitemap = 1

expected_keys = ('redirect_flow_id', 'reference_doctype', 'reference_docname')

def get_context(context):
	context.no_cache = 1

	# all these keys exist in form_dict
	if not (set(expected_keys) - set(dataent.form_dict.keys())):
		for key in expected_keys:
			context[key] = dataent.form_dict[key]

	else:
		dataent.redirect_to_message(_('Some information is missing'),
			_('Looks like someone sent you to an incomplete URL. Please ask them to look into it.'))
		dataent.local.flags.redirect_location = dataent.local.response.location
		raise dataent.Redirect

@dataent.whitelist(allow_guest=True)
def confirm_payment(redirect_flow_id, reference_doctype, reference_docname):

	client = gocardless_initialization(reference_docname)

	try:
		redirect_flow = client.redirect_flows.complete(
			redirect_flow_id,
			params={
				"session_token": dataent.session.user
		})

		confirmation_url = redirect_flow.confirmation_url
		gocardless_success_page = dataent.get_hooks('gocardless_success_page')
		if gocardless_success_page:
			confirmation_url = dataent.get_attr(gocardless_success_page[-1])(reference_doctype, reference_docname)

		data = {
			"mandate": redirect_flow.links.mandate,
			"customer": redirect_flow.links.customer,
			"redirect_to": confirmation_url,
			"redirect_message": "Mandate successfully created",
			"reference_doctype": reference_doctype,
			"reference_docname": reference_docname
		}

		try:
			create_mandate(data)
		except Exception as e:
			dataent.log_error(e, "GoCardless Mandate Registration Error")

		gateway_controller = get_gateway_controller(reference_docname)
		dataent.get_doc("GoCardless Settings", gateway_controller).create_payment_request(data)

		return {"redirect_to": confirmation_url}

	except Exception as e:
		dataent.log_error(e, "GoCardless Payment Error")
		return {"redirect_to": '/integrations/payment-failed'}


def create_mandate(data):
	data = dataent._dict(data)
	dataent.logger().debug(data)

	mandate = data.get('mandate')

	if dataent.db.exists("GoCardless Mandate", mandate):
		return

	else:
		reference_doc = dataent.db.get_value(data.get('reference_doctype'), data.get('reference_docname'), ["reference_doctype", "reference_name"], as_dict=1)
		epaas_customer = dataent.db.get_value(reference_doc.reference_doctype, reference_doc.reference_name, ["customer_name"], as_dict=1)

		try:
			dataent.get_doc({
			"doctype": "GoCardless Mandate",
			"mandate": mandate,
			"customer": epaas_customer.customer_name,
			"gocardless_customer": data.get('customer')
			}).insert(ignore_permissions=True)

		except Exception:
			dataent.log_error(dataent.get_traceback())