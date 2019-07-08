# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals

import dataent


@dataent.whitelist(allow_guest=True)
def send_message(subject="Website Query", message="", sender="", status="Open"):
	from dataent.www.contact import send_message as website_send_message
	lead = customer = None

	website_send_message(subject, message, sender)

	customer = dataent.db.sql("""select distinct dl.link_name from `tabDynamic Link` dl
		left join `tabContact` c on dl.parent=c.name where dl.link_doctype='Customer'
		and c.email_id = %s""", sender)

	if not customer:
		lead = dataent.db.get_value('Lead', dict(email_id=sender))
		if not lead:
			new_lead = dataent.get_doc(dict(
				doctype='Lead',
				email_id = sender,
				lead_name = sender.split('@')[0].title()
			)).insert(ignore_permissions=True)

	opportunity = dataent.get_doc(dict(
		doctype ='Opportunity',
		opportunity_from = 'Customer' if customer else 'Lead',
		status = 'Open',
		title = subject,
		contact_email = sender,
		to_discuss = message
	))

	if customer:
		opportunity.party_name = customer[0][0]
	elif lead:
		opportunity.party_name = lead
	else:
		opportunity.party_name = new_lead.name

	opportunity.insert(ignore_permissions=True)

	comm = dataent.get_doc({
		"doctype":"Communication",
		"subject": subject,
		"content": message,
		"sender": sender,
		"sent_or_received": "Received",
		'reference_doctype': 'Opportunity',
		'reference_name': opportunity.name
	})
	comm.insert(ignore_permissions=True)

	return "okay"
