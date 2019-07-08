// Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

dataent.provide("epaas.maintenance");

dataent.ui.form.on('Maintenance Visit', {
	setup: function(frm) {
		frm.set_query('contact_person', epaas.queries.contact_query);
		frm.set_query('customer_address', epaas.queries.address_query);
	},
	customer: function(frm) {
		epaas.utils.get_party_details(frm)
	},
	customer_address: function(frm) {
		epaas.utils.get_address_display(frm, 'customer_address', 'address_display');
	},
	contact_person: function(frm) {
		epaas.utils.get_contact_details(frm);
	}

})

// TODO commonify this code
epaas.maintenance.MaintenanceVisit = dataent.ui.form.Controller.extend({
	refresh: function() {
		dataent.dynamic_link = {doc: this.frm.doc, fieldname: 'customer', doctype: 'Customer'}

		var me = this;

		if (this.frm.doc.docstatus===0) {
			this.frm.add_custom_button(__('Maintenance Schedule'),
				function() {
					epaas.utils.map_current_doc({
						method: "epaas.maintenance.doctype.maintenance_schedule.maintenance_schedule.make_maintenance_visit",
						source_doctype: "Maintenance Schedule",
						target: me.frm,
						setters: {
							customer: me.frm.doc.customer || undefined,
						},
						get_query_filters: {
							docstatus: 1,
							company: me.frm.doc.company
						}
					})
				}, __("Get items from"));
			this.frm.add_custom_button(__('Warranty Claim'),
				function() {
					epaas.utils.map_current_doc({
						method: "epaas.support.doctype.warranty_claim.warranty_claim.make_maintenance_visit",
						source_doctype: "Warranty Claim",
						target: me.frm,
						date_field: "complaint_date",
						setters: {
							customer: me.frm.doc.customer || undefined,
						},
						get_query_filters: {
							status: ["in", "Open, Work in Progress"],
							company: me.frm.doc.company
						}
					})
				}, __("Get items from"));
			this.frm.add_custom_button(__('Sales Order'),
				function() {
					epaas.utils.map_current_doc({
						method: "epaas.selling.doctype.sales_order.sales_order.make_maintenance_visit",
						source_doctype: "Sales Order",
						target: me.frm,
						setters: {
							customer: me.frm.doc.customer || undefined,
						},
						get_query_filters: {
							docstatus: 1,
							company: me.frm.doc.company,
							order_type: me.frm.doc.order_type,
						}
					})
				}, __("Get items from"));
		}
	},
});

$.extend(cur_frm.cscript, new epaas.maintenance.MaintenanceVisit({frm: cur_frm}));

cur_frm.cscript.onload = function(doc, dt, dn) {
	if(!doc.status) set_multiple(dt,dn,{status:'Draft'});
	if(doc.__islocal) set_multiple(dt,dn,{mntc_date: dataent.datetime.get_today()});

	// set add fetch for item_code's item_name and description
	cur_frm.add_fetch('item_code', 'item_name', 'item_name');
	cur_frm.add_fetch('item_code', 'description', 'description');
}

cur_frm.fields_dict.customer.get_query = function(doc,cdt,cdn) {
	return {query: "epaas.controllers.queries.customer_query" }
}
