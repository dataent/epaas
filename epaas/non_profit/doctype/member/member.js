// Copyright (c) 2017, Dataent Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

dataent.ui.form.on('Member', {
	refresh: function(frm) {

		dataent.dynamic_link = {doc: frm.doc, fieldname: 'name', doctype: 'Member'};

		frm.toggle_display(['address_html','contact_html'], !frm.doc.__islocal);

		if(!frm.doc.__islocal) {
			dataent.contacts.render_address_and_contact(frm);

			// custom buttons
			frm.add_custom_button(__('Accounting Ledger'), function() {
				dataent.set_route('query-report', 'General Ledger',
					{party_type:'Member', party:frm.doc.name});
			});

			frm.add_custom_button(__('Accounts Receivable'), function() {
				dataent.set_route('query-report', 'Accounts Receivable', {member:frm.doc.name});
			});

			// indicator
			epaas.utils.set_party_dashboard_indicators(frm);

		} else {
			dataent.contacts.clear_address_and_contact(frm);
		}

		dataent.call({
			method:"dataent.client.get_value",
			args:{
				'doctype':"Membership",
				'filters':{'member': frm.doc.name},
				'fieldname':[
					'to_date'
				]
			},
			callback: function (data) {
				if(data.message) {
					dataent.model.set_value(frm.doctype,frm.docname,
						"membership_expiry_date", data.message.to_date);
				}
			}
		});
	}
});