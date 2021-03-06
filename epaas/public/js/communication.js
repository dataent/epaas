dataent.ui.form.on("Communication", {
	refresh: (frm) => {
		// setup custom Make button only if Communication is Email
		if(frm.doc.communication_medium == "Email" && frm.doc.sent_or_received == "Received") {
			frm.events.setup_custom_buttons(frm);
		}
	},

	setup_custom_buttons: (frm) => {
		let confirm_msg = "Are you sure you want to create {0} from this email";
		if(frm.doc.reference_doctype !== "Issue") {
			frm.add_custom_button(__("Issue"), () => {
				dataent.confirm(__(confirm_msg, [__("Issue")]), () => {
					frm.trigger('make_issue_from_communication');
				})
			}, "Make");
		}

		if(!in_list(["Lead", "Opportunity"], frm.doc.reference_doctype)) {
			frm.add_custom_button(__("Lead"), () => {
				dataent.confirm(__(confirm_msg, [__("Lead")]), () => {
					frm.trigger('make_lead_from_communication');
				})
			}, __("Make"));

			frm.add_custom_button(__("Opportunity"), () => {
				dataent.confirm(__(confirm_msg, [__("Opportunity")]), () => {
					frm.trigger('make_opportunity_from_communication');
				})
			}, __("Make"));
		}
	},

	make_lead_from_communication: (frm) => {
		return dataent.call({
			method: "epaas.crm.doctype.lead.lead.make_lead_from_communication",
			args: {
				communication: frm.doc.name
			},
			freeze: true,
			callback: (r) => {
				if(r.message) {
					frm.reload_doc()
				}
			}
		})
	},

	make_issue_from_communication: (frm) => {
		return dataent.call({
			method: "epaas.support.doctype.issue.issue.make_issue_from_communication",
			args: {
				communication: frm.doc.name
			},
			freeze: true,
			callback: (r) => {
				if(r.message) {
					frm.reload_doc()
				}
			}
		})
	},

	make_opportunity_from_communication: (frm) => {
		return dataent.call({
			method: "epaas.crm.doctype.opportunity.opportunity.make_opportunity_from_communication",
			args: {
				communication: frm.doc.name
			},
			freeze: true,
			callback: (r) => {
				if(r.message) {
					frm.reload_doc()
				}
			}
		})
	}
});