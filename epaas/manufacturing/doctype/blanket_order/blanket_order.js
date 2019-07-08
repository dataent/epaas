// Copyright (c) 2018, Dataent Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

dataent.ui.form.on('Blanket Order', {
	setup: function(frm) {
		frm.add_fetch("customer", "customer_name", "customer_name");
		frm.add_fetch("supplier", "supplier_name", "supplier_name");
	},

	refresh: function(frm) {
		if (frm.doc.customer && frm.doc.docstatus === 1) {
			frm.add_custom_button(__('View Orders'), function() {
				dataent.set_route('List', 'Sales Order', {blanket_order: frm.doc.name});
			});
			frm.add_custom_button(__("Create Sales Order"), function(){
				dataent.model.open_mapped_doc({
					method: "epaas.manufacturing.doctype.blanket_order.blanket_order.make_sales_order",
					frm: frm
				});
			}).addClass("btn-primary");
		}

		if (frm.doc.supplier && frm.doc.docstatus === 1) {
			frm.add_custom_button(__('View Orders'), function() {
				dataent.set_route('List', 'Purchase Order', {blanket_order: frm.doc.name});
			});
			frm.add_custom_button(__("Create Purchase Order"), function(){
				dataent.model.open_mapped_doc({
					method: "epaas.manufacturing.doctype.blanket_order.blanket_order.make_purchase_order",
					frm: frm
				});
			}).addClass("btn-primary");
		}
	},

	onload_post_render: function(frm) {
		frm.get_field("items").grid.set_multiple_add("item_code", "qty");
	}
});
