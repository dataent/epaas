// Copyright (c) 2015, Dataent Technologies and contributors
// For license information, please see license.txt

cur_frm.add_fetch('fee_structure', 'total_amount', 'amount');

dataent.ui.form.on("Program", "refresh", function(frm) {
	if(!frm.doc.__islocal) {
		frm.add_custom_button(__("Student Applicant"), function() {
			dataent.route_options = {
				program: frm.doc.name
			}
			dataent.set_route("List", "Student Applicant");
		});
		
		frm.add_custom_button(__("Program Enrollment"), function() {
			dataent.route_options = {
				program: frm.doc.name
			}
			dataent.set_route("List", "Program Enrollment");
		});
		
		frm.add_custom_button(__("Student Group"), function() {
			dataent.route_options = {
				program: frm.doc.name
			}
			dataent.set_route("List", "Student Group");
		});
		
		frm.add_custom_button(__("Fee Structure"), function() {
			dataent.route_options = {
				program: frm.doc.name
			}
			dataent.set_route("List", "Fee Structure");
		});
		
		frm.add_custom_button(__("Fees"), function() {
			dataent.route_options = {
				program: frm.doc.name
			}
			dataent.set_route("List", "Fees");
		});
	}
});