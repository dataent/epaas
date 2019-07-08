// Copyright (c) 2017, Dataent Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

dataent.ui.form.on('Volunteer', {
	refresh: function(frm) {

		dataent.dynamic_link = {doc: frm.doc, fieldname: 'name', doctype: 'Volunteer'};

		frm.toggle_display(['address_html','contact_html'], !frm.doc.__islocal);

		if(!frm.doc.__islocal) {
			dataent.contacts.render_address_and_contact(frm);
		} else {
			dataent.contacts.clear_address_and_contact(frm);
		}
	}
});
