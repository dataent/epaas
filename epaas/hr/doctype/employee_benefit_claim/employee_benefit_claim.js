// Copyright (c) 2018, Dataent Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

dataent.ui.form.on('Employee Benefit Claim', {
	setup: function(frm) {
		frm.set_query("earning_component", function() {
			return {
				query : "epaas.hr.doctype.employee_benefit_application.employee_benefit_application.get_earning_components",
				filters: {date: frm.doc.claim_date, employee: frm.doc.employee}
			};
		});
	},
	employee: function(frm) {
		frm.set_value("earning_component", null);
	}
});
