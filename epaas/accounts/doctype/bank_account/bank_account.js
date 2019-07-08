// Copyright (c) 2018, Dataent Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

dataent.ui.form.on('Bank Account', {
	setup: function(frm) {
		frm.set_query("account", function() {
			return {
				filters: {
					'account_type': 'Bank',
					'company': frm.doc.company,
					'is_group': 0
				}
			};
		});
		frm.set_query("party_type", function() {
			return {
				query: "epaas.setup.doctype.party_type.party_type.get_party_type",
			};
		});
	},
	refresh: function(frm) {
		dataent.dynamic_link = { doc: frm.doc, fieldname: 'name', doctype: 'Bank Account' }
		
		frm.toggle_display(['address_html','contact_html'], !frm.doc.__islocal);

		if (frm.doc.__islocal) {
			dataent.contacts.clear_address_and_contact(frm);
		}
		else {
			dataent.contacts.render_address_and_contact(frm);
		}

		if (frm.doc.integration_id) {
			frm.add_custom_button(__("Unlink external integrations"), function() {
				dataent.confirm(__("This action will unlink this account from any external service integrating EPAAS with your bank accounts. It cannot be undone. Are you certain ?"), function() {
					frm.set_value("integration_id", "");
				});
			});
		}
	}
});
