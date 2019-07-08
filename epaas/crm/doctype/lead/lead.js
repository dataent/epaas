// Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

dataent.provide("epaas");
cur_frm.email_field = "email_id";

epaas.LeadController = dataent.ui.form.Controller.extend({
	setup: function () {

		this.frm.make_methods = {
			'Quotation': () => epaas.utils.create_new_doc('Quotation', {
				'quotation_to': this.frm.doc.doctype,
				'party_name': this.frm.doc.name
			}),
			'Opportunity': () => epaas.utils.create_new_doc('Opportunity', {
				'opportunity_from': this.frm.doc.doctype,
				'party_name': this.frm.doc.name
			})
		}

		this.frm.fields_dict.customer.get_query = function (doc, cdt, cdn) {
			return { query: "epaas.controllers.queries.customer_query" }
		}

		this.frm.toggle_reqd("lead_name", !this.frm.doc.organization_lead);
	},

	onload: function () {
		if (cur_frm.fields_dict.lead_owner.df.options.match(/^User/)) {
			cur_frm.fields_dict.lead_owner.get_query = function (doc, cdt, cdn) {
				return { query: "dataent.core.doctype.user.user.user_query" }
			}
		}

		if (cur_frm.fields_dict.contact_by.df.options.match(/^User/)) {
			cur_frm.fields_dict.contact_by.get_query = function (doc, cdt, cdn) {
				return { query: "dataent.core.doctype.user.user.user_query" }
			}
		}
	},

	refresh: function () {
		var doc = this.frm.doc;
		epaas.toggle_naming_series();
		dataent.dynamic_link = { doc: doc, fieldname: 'name', doctype: 'Lead' }

		if (!doc.__islocal && doc.__onload && !doc.__onload.is_customer) {
			this.frm.add_custom_button(__("Customer"), this.create_customer, __("Make"));
			this.frm.add_custom_button(__("Opportunity"), this.create_opportunity, __("Make"));
			this.frm.add_custom_button(__("Quotation"), this.make_quotation, __("Make"));
		}

		if (!this.frm.doc.__islocal) {
			dataent.contacts.render_address_and_contact(cur_frm);
		} else {
			dataent.contacts.clear_address_and_contact(cur_frm);
		}
	},

	create_customer: function () {
		dataent.model.open_mapped_doc({
			method: "epaas.crm.doctype.lead.lead.make_customer",
			frm: cur_frm
		})
	},

	create_opportunity: function () {
		dataent.model.open_mapped_doc({
			method: "epaas.crm.doctype.lead.lead.make_opportunity",
			frm: cur_frm
		})
	},

	make_quotation: function () {
		dataent.model.open_mapped_doc({
			method: "epaas.crm.doctype.lead.lead.make_quotation",
			frm: cur_frm
		})
	},

	organization_lead: function () {
		this.frm.toggle_reqd("lead_name", !this.frm.doc.organization_lead);
		this.frm.toggle_reqd("company_name", this.frm.doc.organization_lead);
	},

	company_name: function () {
		if (this.frm.doc.organization_lead == 1) {
			this.frm.set_value("lead_name", this.frm.doc.company_name);
		}
	},

	contact_date: function () {
		if (this.frm.doc.contact_date) {
			let d = moment(this.frm.doc.contact_date);
			d.add(1, "hours");
			this.frm.set_value("ends_on", d.format(dataent.defaultDatetimeFormat));
		}
	}
});

$.extend(cur_frm.cscript, new epaas.LeadController({ frm: cur_frm }));
