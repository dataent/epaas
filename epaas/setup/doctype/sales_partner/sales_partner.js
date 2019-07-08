// Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

dataent.ui.form.on('Sales Partner', {
	refresh: function(frm) {
		dataent.dynamic_link = {doc: frm.doc, fieldname: 'name', doctype: 'Sales Partner'}

		if(frm.doc.__islocal){
			hide_field(['address_html', 'contact_html', 'address_contacts']);
			dataent.contacts.clear_address_and_contact(frm);
		}
		else{
			unhide_field(['address_html', 'contact_html', 'address_contacts']);
			dataent.contacts.render_address_and_contact(frm);
		}
	}
});
