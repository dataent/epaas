# Copyright (c) 2018, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt
from __future__ import unicode_literals
import dataent
from dataent import _
from dataent.utils import flt
import json
from epaas.epaas_integrations.doctype.gocardless_settings.gocardless_settings import gocardless_initialization, get_gateway_controller
from dataent.utils import get_url

no_cache = 1
no_sitemap = 1

expected_keys = ('amount', 'title', 'description', 'reference_doctype', 'reference_docname',
	'payer_name', 'payer_email', 'order_id', 'currency')

def get_context(context):
	context.no_cache = 1

	# all these keys exist in form_dict
	if not (set(expected_keys) - set(dataent.form_dict.keys())):
		for key in expected_keys:
			context[key] = dataent.form_dict[key]

		context['amount'] = flt(context['amount'])

		gateway_controller = get_gateway_controller(context.reference_docname)
		context['header_img'] = dataent.db.get_value("GoCardless Settings", gateway_controller, "header_img")

	else:
		dataent.redirect_to_message(_('Some information is missing'),
			_('Looks like someone sent you to an incomplete URL. Please ask them to look into it.'))
		dataent.local.flags.redirect_location = dataent.local.response.location
		raise dataent.Redirect

@dataent.whitelist(allow_guest=True)
def check_mandate(data, reference_doctype, reference_docname):
	data = json.loads(data)

	client = gocardless_initialization(reference_docname)

	payer = dataent.get_doc("Customer", data["payer_name"])

	if payer.customer_type == "Individual" and payer.customer_primary_contact is not None:
		primary_contact = dataent.get_doc("Contact", payer.customer_primary_contact)
		prefilled_customer = {
			"company_name": payer.name,
			"given_name": primary_contact.first_name,
		}
		if primary_contact.last_name is not None:
			prefilled_customer.update({"family_name": primary_contact.last_name})

		if primary_contact.email_id is not None:
			prefilled_customer.update({"email": primary_contact.email_id})
		else:
			prefilled_customer.update({"email": dataent.session.user})

	else:
		prefilled_customer = {
			"company_name": payer.name,
			"email": dataent.session.user
		}

	success_url = get_url("./integrations/gocardless_confirmation?reference_doctype=" + reference_doctype + "&reference_docname=" + reference_docname)

	try:
		redirect_flow = client.redirect_flows.create(params={
							"description": _("Pay {0} {1}".format(data['amount'], data['currency'])),
							"session_token": dataent.session.user,
							"success_redirect_url": success_url,
							"prefilled_customer": prefilled_customer
						})

		return {"redirect_to": redirect_flow.redirect_url}

	except Exception as e:
		dataent.log_error(e, "GoCardless Payment Error")
		return {"redirect_to": '/integrations/payment-failed'}