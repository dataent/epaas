// Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

dataent.ui.form.on('Cashier Closing', {

	setup: function(frm){
		if (frm.doc.user == "" || frm.doc.user == null) {
			frm.doc.user = dataent.session.user;
		}
	}
});
