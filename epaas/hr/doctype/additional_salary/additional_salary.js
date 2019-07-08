// Copyright (c) 2018, Dataent Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

dataent.ui.form.on('Additional Salary', {
	setup: function(frm) {
		frm.add_fetch("salary_component", "deduct_full_tax_on_selected_payroll_date", "deduct_full_tax_on_selected_payroll_date");

		frm.set_query("employee", function() {
			return {
				filters: {
					company: frm.doc.company
				}
			};
		});
	}
});
