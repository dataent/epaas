// Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

dataent.ui.form.on("Supplier", {
	setup: function (frm) {
		frm.set_query('default_price_list', { 'buying': 1 });
		if (frm.doc.__islocal == 1) {
			frm.set_value("represents_company", "");
		}
		frm.set_query('account', 'accounts', function (doc, cdt, cdn) {
			var d = locals[cdt][cdn];
			return {
				filters: {
					'account_type': 'Payable',
					'company': d.company,
					"is_group": 0
				}
			}
		});
	},
	refresh: function (frm) {
		dataent.dynamic_link = { doc: frm.doc, fieldname: 'name', doctype: 'Supplier' }

		if (dataent.defaults.get_default("supp_master_name") != "Naming Series") {
			frm.toggle_display("naming_series", false);
		} else {
			epaas.toggle_naming_series();
		}

		if (frm.doc.__islocal) {
			hide_field(['address_html','contact_html']);
			dataent.contacts.clear_address_and_contact(frm);
		}
		else {
			unhide_field(['address_html','contact_html']);
			dataent.contacts.render_address_and_contact(frm);

			// custom buttons
			frm.add_custom_button(__('Accounting Ledger'), function () {
				dataent.set_route('query-report', 'General Ledger',
					{ party_type: 'Supplier', party: frm.doc.name });
			}, __("View"));

			frm.add_custom_button(__('Accounts Payable'), function () {
				dataent.set_route('query-report', 'Accounts Payable', { supplier: frm.doc.name });
			}, __("View"));

			frm.add_custom_button(__('Bank Account'), function () {
				epaas.utils.make_bank_account(frm.doc.doctype, frm.doc.name);
			}, __("Make"));

			frm.add_custom_button(__('Pricing Rule'), function () {
				epaas.utils.make_pricing_rule(frm.doc.doctype, frm.doc.name);
			}, __("Make"));

			// indicators
			epaas.utils.set_party_dashboard_indicators(frm);
		}
	},

	is_internal_supplier: function(frm) {
		if (frm.doc.is_internal_supplier == 1) {
			frm.toggle_reqd("represents_company", true);
		}
		else {
			frm.toggle_reqd("represents_company", false);
		}
	}
});
