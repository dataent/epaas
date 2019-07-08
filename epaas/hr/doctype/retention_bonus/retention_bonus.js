// Copyright (c) 2018, Dataent Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

dataent.ui.form.on('Retention Bonus', {
	setup: function(frm) {
		frm.set_query("employee", function() {
			return {
				filters: {
					"status": "Active"
				}
			};
		});
	},
	refresh: function(frm) {

	}
});
