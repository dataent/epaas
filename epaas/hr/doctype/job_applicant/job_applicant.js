// Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

// For license information, please see license.txt

// for communication
cur_frm.email_field = "email_id";

dataent.ui.form.on("Job Applicant", {
	refresh: function(frm) {
		if (!frm.doc.__islocal) {
			if (frm.doc.__onload && frm.doc.__onload.job_offer) {
				frm.add_custom_button(__("Job Offer"), function() {
					dataent.set_route("Form", "Job Offer", frm.doc.__onload.job_offer);
				}, __("View"));
			} else {
				frm.add_custom_button(__("Job Offer"), function() {
					dataent.route_options = {
						"job_applicant": frm.doc.name,
						"applicant_name": frm.doc.applicant_name,
						"designation": frm.doc.job_opening,
					};
					dataent.new_doc("Job Offer");
				});
			}
		}

		frm.set_query("job_title", function() {
			return {
				filters: {
					'status': 'Open'
				}
			};
		});

	}
});