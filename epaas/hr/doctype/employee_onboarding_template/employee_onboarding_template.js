// Copyright (c) 2018, Dataent Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

dataent.ui.form.on('Employee Onboarding Template', {
	setup: function(frm) {
		frm.set_query("department", function() {
			return {
				filters: {
					company: frm.doc.company
				}
			};
		});
	}
});
