// Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt



dataent.ui.form.on_change("Installation Note", "customer",
	function(frm) { epaas.utils.get_party_details(frm); });

dataent.ui.form.on_change("Installation Note", "customer_address",
	function(frm) { epaas.utils.get_address_display(frm); });

dataent.ui.form.on_change("Installation Note", "contact_person",
	function(frm) { epaas.utils.get_contact_details(frm); });

dataent.provide("epaas.selling");
// TODO commonify this code
epaas.selling.InstallationNote = dataent.ui.form.Controller.extend({
	onload: function() {
		if(!this.frm.doc.status) {
			set_multiple(this.frm.doc.doctype, this.frm.doc.name, { status:'Draft'});
		}
		if(this.frm.doc.__islocal) {
			set_multiple(this.frm.doc.doctype, this.frm.doc.name,
				{inst_date: dataent.datetime.get_today()});
		}

		this.setup_queries();
	},

	setup_queries: function() {
		var me = this;

		dataent.dynamic_link = {doc: this.frm.doc, fieldname: 'customer', doctype: 'Customer'}
		frm.set_query('customer_address', epaas.queries.address_query);
		this.frm.set_query('contact_person', epaas.queries.contact_query);

		this.frm.set_query("customer", function() {
			return {
				query: "epaas.controllers.queries.customer_query"
			}
		});
	},

	refresh: function() {
		var me = this;
		if (this.frm.doc.docstatus===0) {
			this.frm.add_custom_button(__('From Delivery Note'),
				function() {
					epaas.utils.map_current_doc({
						method: "epaas.stock.doctype.delivery_note.delivery_note.make_installation_note",
						source_doctype: "Delivery Note",
						target: me.frm,
						date_field: "posting_date",
						setters: {
							customer: me.frm.doc.customer || undefined,
						},
						get_query_filters: {
							docstatus: 1,
							status: ["not in", ["Stopped", "Closed"]],
							per_installed: ["<", 99.99],
							company: me.frm.doc.company
						}
					})
				}, "fa fa-download", "btn-default"
			);
		}
	},
});

$.extend(cur_frm.cscript, new epaas.selling.InstallationNote({frm: cur_frm}));