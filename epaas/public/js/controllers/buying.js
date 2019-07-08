// Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

dataent.provide("epaas.buying");

cur_frm.cscript.tax_table = "Purchase Taxes and Charges";

{% include 'epaas/accounts/doctype/purchase_taxes_and_charges_template/purchase_taxes_and_charges_template.js' %}

cur_frm.email_field = "contact_email";

epaas.buying.BuyingController = epaas.TransactionController.extend({
	setup: function() {
		this._super();
	},

	onload: function() {
		this.setup_queries();
		this._super();

		this.frm.set_query('shipping_rule', function() {
			return {
				filters: {
					"shipping_rule_type": "Buying"
				}
			};
		});

		if (this.frm.doc.__islocal
			&& dataent.meta.has_field(this.frm.doc.doctype, "disable_rounded_total")) {

				var df = dataent.meta.get_docfield(this.frm.doc.doctype, "disable_rounded_total");
				var disable = df.default || cint(dataent.sys_defaults.disable_rounded_total);
				this.frm.set_value("disable_rounded_total", disable);
		}

		/* eslint-disable */
		// no idea where me is coming from
		if(this.frm.get_field('shipping_address')) {
			this.frm.set_query("shipping_address", function() {
				if(me.frm.doc.customer) {
					return {
						query: 'dataent.contacts.doctype.address.address.address_query',
						filters: { link_doctype: 'Customer', link_name: me.frm.doc.customer }
					};
				} else
					return epaas.queries.company_address_query(me.frm.doc)
			});
		}
		/* eslint-enable */
	},

	setup_queries: function() {
		var me = this;

		if(this.frm.fields_dict.buying_price_list) {
			this.frm.set_query("buying_price_list", function() {
				return{
					filters: { 'buying': 1 }
				}
			});
		}

		me.frm.set_query('supplier', epaas.queries.supplier);
		me.frm.set_query('contact_person', epaas.queries.contact_query);
		me.frm.set_query('supplier_address', epaas.queries.address_query);

		if(this.frm.fields_dict.supplier) {
			this.frm.set_query("supplier", function() {
				return{	query: "epaas.controllers.queries.supplier_query" }});
		}

		this.frm.set_query("item_code", "items", function() {
			if(me.frm.doc.is_subcontracted == "Yes") {
				return{
					query: "epaas.controllers.queries.item_query",
					filters:{ 'is_sub_contracted_item': 1 }
				}
			} else {
				return{
					query: "epaas.controllers.queries.item_query",
					filters: {'is_purchase_item': 1}
				}
			}
		});
	},

	refresh: function(doc) {
		dataent.dynamic_link = {doc: this.frm.doc, fieldname: 'supplier', doctype: 'Supplier'};

		this.frm.toggle_display("supplier_name",
			(this.frm.doc.supplier_name && this.frm.doc.supplier_name!==this.frm.doc.supplier));

		if(this.frm.doc.docstatus==0 &&
			(this.frm.doctype==="Purchase Order" || this.frm.doctype==="Material Request")) {
			this.set_from_product_bundle();
		}

		this._super();
	},

	supplier: function() {
		var me = this;
		epaas.utils.get_party_details(this.frm, null, null, function(){
			me.apply_price_list();
		});
	},

	supplier_address: function() {
		epaas.utils.get_address_display(this.frm);
	},

	buying_price_list: function() {
		this.apply_price_list();
	},

	price_list_rate: function(doc, cdt, cdn) {
		var item = dataent.get_doc(cdt, cdn);
		dataent.model.round_floats_in(item, ["price_list_rate", "discount_percentage"]);

		let item_rate = item.price_list_rate;
		if (doc.doctype == "Purchase Order" && item.blanket_order_rate) {
			item_rate = item.blanket_order_rate;
		}
		item.discount_amount = flt(item_rate) * flt(item.discount_percentage) / 100;
		item.rate = flt((item.price_list_rate) - (item.discount_amount), precision('rate', item));

		this.calculate_taxes_and_totals();
	},

	discount_percentage: function(doc, cdt, cdn) {
		this.price_list_rate(doc, cdt, cdn);
	},

	qty: function(doc, cdt, cdn) {
		var item = dataent.get_doc(cdt, cdn);
		if ((doc.doctype == "Purchase Receipt") || (doc.doctype == "Purchase Invoice" && (doc.update_stock || doc.is_return))) {
			dataent.model.round_floats_in(item, ["qty", "received_qty"]);

			if(!doc.is_return && this.validate_negative_quantity(cdt, cdn, item, ["qty", "received_qty"])){ return }

			if(!item.rejected_qty && item.qty) {
				item.received_qty = item.qty;
			}

			dataent.model.round_floats_in(item, ["qty", "received_qty"]);
			item.rejected_qty = flt(item.received_qty - item.qty, precision("rejected_qty", item));
		}

		this._super(doc, cdt, cdn);
	},

	received_qty: function(doc, cdt, cdn) {
		this.calculate_accepted_qty(doc, cdt, cdn)
	},

	rejected_qty: function(doc, cdt, cdn) {
		this.calculate_accepted_qty(doc, cdt, cdn)
	},

	calculate_accepted_qty: function(doc, cdt, cdn){
		var item = dataent.get_doc(cdt, cdn);
		dataent.model.round_floats_in(item, ["received_qty", "rejected_qty"]);

		if(!doc.is_return && this.validate_negative_quantity(cdt, cdn, item, ["received_qty", "rejected_qty"])){ return }

		item.qty = flt(item.received_qty - item.rejected_qty, precision("qty", item));
		this.qty(doc, cdt, cdn);
	},

	validate_negative_quantity: function(cdt, cdn, item, fieldnames){
		if(!item || !fieldnames) { return }

		var is_negative_qty = false;
		for(var i = 0; i<fieldnames.length; i++) {
			if(item[fieldnames[i]] < 0){
				dataent.msgprint(__("Row #{0}: {1} can not be negative for item {2}",
					[item.idx,__(dataent.meta.get_label(cdt, fieldnames[i], cdn)), item.item_code]));
				is_negative_qty = true;
				break;
			}
		}

		return is_negative_qty
	},

	warehouse: function(doc, cdt, cdn) {
		var item = dataent.get_doc(cdt, cdn);
		if(item.item_code && item.warehouse) {
			return this.frm.call({
				method: "epaas.stock.get_item_details.get_bin_details",
				child: item,
				args: {
					item_code: item.item_code,
					warehouse: item.warehouse
				}
			});
		}
	},

	project: function(doc, cdt, cdn) {
		var item = dataent.get_doc(cdt, cdn);
		if(item.project) {
			$.each(this.frm.doc["items"] || [],
				function(i, other_item) {
					if(!other_item.project) {
						other_item.project = item.project;
						refresh_field("project", other_item.name, other_item.parentfield);
					}
				});
		}
	},

	category: function(doc, cdt, cdn) {
		// should be the category field of tax table
		if(cdt != doc.doctype) {
			this.calculate_taxes_and_totals();
		}
	},
	add_deduct_tax: function(doc, cdt, cdn) {
		this.calculate_taxes_and_totals();
	},

	set_from_product_bundle: function() {
		var me = this;
		this.frm.add_custom_button(__("Product Bundle"), function() {
			epaas.buying.get_items_from_product_bundle(me.frm);
		}, __("Get items from"));
	},

	shipping_address: function(){
		var me = this;
		epaas.utils.get_address_display(this.frm, "shipping_address",
			"shipping_address_display", true);
	},

	tc_name: function() {
		this.get_terms();
	},

	link_to_mrs: function() {
		var my_items = [];
		for (var i in cur_frm.doc.items) {
			if(!cur_frm.doc.items[i].material_request){
				my_items.push(cur_frm.doc.items[i].item_code);
			}
		}
		dataent.call({
			method: "epaas.buying.utils.get_linked_material_requests",
			args:{
				items: my_items
			},
			callback: function(r) {
				if(!r.message) {
					dataent.throw(__("No pending Material Requests found to link for the given items."))
				}
				else {
					var i = 0;
					var item_length = cur_frm.doc.items.length;
					while (i < item_length) {
						var qty = cur_frm.doc.items[i].qty;
						(r.message[0] || []).forEach(function(d) {
							if (d.qty > 0 && qty > 0 && cur_frm.doc.items[i].item_code == d.item_code && !cur_frm.doc.items[i].material_request_item)
							{
								cur_frm.doc.items[i].material_request = d.mr_name;
								cur_frm.doc.items[i].material_request_item = d.mr_item;
								var my_qty = Math.min(qty, d.qty);
								qty = qty - my_qty;
								d.qty = d.qty  - my_qty;
								cur_frm.doc.items[i].stock_qty = my_qty*cur_frm.doc.items[i].conversion_factor;
								cur_frm.doc.items[i].qty = my_qty;

								dataent.msgprint("Assigning " + d.mr_name + " to " + d.item_code + " (row " + cur_frm.doc.items[i].idx + ")");
								if (qty > 0)
								{
									dataent.msgprint("Splitting " + qty + " units of " + d.item_code);
									var newrow = dataent.model.add_child(cur_frm.doc, cur_frm.doc.items[i].doctype, "items");
									item_length++;

									for (var key in cur_frm.doc.items[i])
									{
										newrow[key] = cur_frm.doc.items[i][key];
									}

									newrow.idx = item_length;
									newrow["stock_qty"] = newrow.conversion_factor*qty;
									newrow["qty"] = qty;

									newrow["material_request"] = "";
									newrow["material_request_item"] = "";

								}
							}
						});
						i++;
					}
					refresh_field("items");
					//cur_frm.save();
				}
			}
		});
	},

	update_auto_repeat_reference: function(doc) {
		if (doc.auto_repeat) {
			dataent.call({
				method:"dataent.desk.doctype.auto_repeat.auto_repeat.update_reference",
				args:{
					docname: doc.auto_repeat,
					reference:doc.name
				},
				callback: function(r){
					if (r.message=="success") {
						dataent.show_alert({message:__("Auto repeat document updated"), indicator:'green'});
					} else {
						dataent.show_alert({message:__("An error occurred during the update process"), indicator:'red'});
					}
				}
			})
		}
	}
});

cur_frm.add_fetch('project', 'cost_center', 'cost_center');

epaas.buying.get_default_bom = function(frm) {
	$.each(frm.doc["items"] || [], function(i, d) {
		if (d.item_code && d.bom === "") {
			return dataent.call({
				type: "GET",
				method: "epaas.stock.get_item_details.get_default_bom",
				args: {
					"item_code": d.item_code,
				},
				callback: function(r) {
					if(r) {
						dataent.model.set_value(d.doctype, d.name, "bom", r.message);
					}
				}
			})
		}
	});
}

epaas.buying.get_items_from_product_bundle = function(frm) {
	var dialog = new dataent.ui.Dialog({
		title: __("Get Items from Product Bundle"),
		fields: [
			{
				"fieldtype": "Link",
				"label": __("Product Bundle"),
				"fieldname": "product_bundle",
				"options":"Product Bundle",
				"reqd": 1
			},
			{
				"fieldtype": "Currency",
				"label": __("Quantity"),
				"fieldname": "quantity",
				"reqd": 1,
				"default": 1
			},
			{
				"fieldtype": "Button",
				"label": __("Get Items"),
				"fieldname": "get_items",
				"cssClass": "btn-primary"
			}
		]
	});

	dialog.fields_dict.get_items.$input.click(function() {
		var args = dialog.get_values();
		if(!args) return;
		dialog.hide();
		return dataent.call({
			type: "GET",
			method: "epaas.stock.doctype.packed_item.packed_item.get_items_from_product_bundle",
			args: {
				args: {
					item_code: args.product_bundle,
					quantity: args.quantity,
					parenttype: frm.doc.doctype,
					parent: frm.doc.name,
					supplier: frm.doc.supplier,
					currency: frm.doc.currency,
					conversion_rate: frm.doc.conversion_rate,
					price_list: frm.doc.buying_price_list,
					price_list_currency: frm.doc.price_list_currency,
					plc_conversion_rate: frm.doc.plc_conversion_rate,
					company: frm.doc.company,
					is_subcontracted: frm.doc.is_subcontracted,
					transaction_date: frm.doc.transaction_date || frm.doc.posting_date,
					ignore_pricing_rule: frm.doc.ignore_pricing_rule
				}
			},
			freeze: true,
			callback: function(r) {
				const first_row_is_empty = function(child_table){
					if($.isArray(child_table) && child_table.length > 0) {
						return !child_table[0].item_code;
					}
					return false;
				};

				const remove_empty_first_row = function(frm){
				if (first_row_is_empty(frm.doc.items)){
					frm.doc.items = frm.doc.items.splice(1);
					}
				};

				if(!r.exc && r.message) {
					remove_empty_first_row(frm);
					for ( var i=0; i< r.message.length; i++ ) {
						var d = frm.add_child("items");
						var item = r.message[i];
						for ( var key in  item) {
							if ( !is_null(item[key]) ) {
								d[key] = item[key];
							}
						}
						if(dataent.meta.get_docfield(d.doctype, "price_list_rate", d.name)) {
							frm.script_manager.trigger("price_list_rate", d.doctype, d.name);
						}
					}
					frm.refresh_field("items");
				}
			}
		})
	});
	dialog.show();
}