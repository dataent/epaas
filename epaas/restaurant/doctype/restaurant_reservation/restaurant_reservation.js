// Copyright (c) 2017, Dataent Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

dataent.ui.form.on('Restaurant Reservation', {
	setup: function(frm) {
		frm.add_fetch('customer', 'customer_name', 'customer_name');
	},
	refresh: function(frm) {

	}
});
