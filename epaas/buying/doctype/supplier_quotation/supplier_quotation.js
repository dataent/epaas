// Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

// attach required files
{% include 'epaas/public/js/controllers/buying.js' %};

dataent.ui.form.on('Suppier Quotation', {
	setup: function(frm) {
		frm.custom_make_buttons = {
			'Purchase Order': 'Purchase Order'
		}
	}
});

epaas.buying.SupplierQuotationController = epaas.buying.BuyingController.extend({
	refresh: function() {
		var me = this;
		this._super();
		if (this.frm.doc.docstatus === 1) {
			cur_frm.add_custom_button(__("Purchase Order"), this.make_purchase_order,
				__("Make"));
			cur_frm.page.set_inner_btn_group_as_primary(__("Make"));
			cur_frm.add_custom_button(__("Quotation"), this.make_quotation,
				__("Make"));
				
			if(!this.frm.doc.auto_repeat) {	
				cur_frm.add_custom_button(__('Subscription'), function() {
					epaas.utils.make_subscription(me.frm.doc.doctype, me.frm.doc.name)
				}, __("Make"))
			}
		}
		else if (this.frm.doc.docstatus===0) {

			this.frm.add_custom_button(__('Material Request'),
				function() {
					epaas.utils.map_current_doc({
						method: "epaas.stock.doctype.material_request.material_request.make_supplier_quotation",
						source_doctype: "Material Request",
						target: me.frm,
						setters: {
							company: me.frm.doc.company
						},
						get_query_filters: {
							material_request_type: "Purchase",
							docstatus: 1,
							status: ["!=", "Stopped"],
							per_ordered: ["<", 99.99]
						}
					})
				}, __("Get items from"));
		}
	},

	make_purchase_order: function() {
		dataent.model.open_mapped_doc({
			method: "epaas.buying.doctype.supplier_quotation.supplier_quotation.make_purchase_order",
			frm: cur_frm
		})
	},
	make_quotation: function() {
		dataent.model.open_mapped_doc({
			method: "epaas.buying.doctype.supplier_quotation.supplier_quotation.make_quotation",
			frm: cur_frm
		})

	}
});

// for backward compatibility: combine new and previous states
$.extend(cur_frm.cscript, new epaas.buying.SupplierQuotationController({frm: cur_frm}));

cur_frm.fields_dict['items'].grid.get_field('project').get_query =
	function(doc, cdt, cdn) {
		return{
			filters:[
				['Project', 'status', 'not in', 'Completed, Cancelled']
			]
		}
	}
