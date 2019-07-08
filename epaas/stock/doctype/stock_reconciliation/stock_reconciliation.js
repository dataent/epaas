// Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

dataent.provide("epaas.stock");

dataent.ui.form.on("Stock Reconciliation", {
	onload: function(frm) {
		frm.add_fetch("item_code", "item_name", "item_name");

		// end of life
		frm.set_query("item_code", "items", function(doc, cdt, cdn) {
			return {
				query: "epaas.controllers.queries.item_query",
				filters:{
					"is_stock_item": 1,
					"has_serial_no": 0
				}
			}
		});

		if (frm.doc.company) {
			epaas.queries.setup_queries(frm, "Warehouse", function() {
				return epaas.queries.warehouse(frm.doc);
			});
		}

		if (!frm.doc.expense_account) {
			frm.trigger("set_expense_account");
		}
	},

	refresh: function(frm) {
		if(frm.doc.docstatus < 1) {
			frm.add_custom_button(__("Items"), function() {
				frm.events.get_items(frm);
			});
		}

		if(frm.doc.company) {
			frm.trigger("toggle_display_account_head");
		}
	},

	get_items: function(frm) {
		dataent.prompt({label:"Warehouse", fieldname: "warehouse", fieldtype:"Link", options:"Warehouse", reqd: 1,
			"get_query": function() {
				return {
					"filters": {
						"company": frm.doc.company,
					}
				}
			}},
			function(data) {
				dataent.call({
					method:"epaas.stock.doctype.stock_reconciliation.stock_reconciliation.get_items",
					args: {
						warehouse: data.warehouse,
						posting_date: frm.doc.posting_date,
						posting_time: frm.doc.posting_time,
						company:frm.doc.company
					},
					callback: function(r) {
						var items = [];
						frm.clear_table("items");
						for(var i=0; i< r.message.length; i++) {
							var d = frm.add_child("items");
							$.extend(d, r.message[i]);
							if(!d.qty) d.qty = null;
							if(!d.valuation_rate) d.valuation_rate = null;
						}
						frm.refresh_field("items");
					}
				});
			}
		, __("Get Items"), __("Update"));
	},

	set_valuation_rate_and_qty: function(frm, cdt, cdn) {
		var d = dataent.model.get_doc(cdt, cdn);
		if(d.item_code && d.warehouse) {
			dataent.call({
				method: "epaas.stock.doctype.stock_reconciliation.stock_reconciliation.get_stock_balance_for",
				args: {
					item_code: d.item_code,
					warehouse: d.warehouse,
					posting_date: frm.doc.posting_date,
					posting_time: frm.doc.posting_time
				},
				callback: function(r) {
					dataent.model.set_value(cdt, cdn, "qty", r.message.qty);
					dataent.model.set_value(cdt, cdn, "valuation_rate", r.message.rate);
					dataent.model.set_value(cdt, cdn, "current_qty", r.message.qty);
					dataent.model.set_value(cdt, cdn, "current_valuation_rate", r.message.rate);
					dataent.model.set_value(cdt, cdn, "current_amount", r.message.rate * r.message.qty);
					dataent.model.set_value(cdt, cdn, "amount", r.message.rate * r.message.qty);

				}
			});
		}
	},
	set_item_code: function(doc, cdt, cdn) {
		var d = dataent.model.get_doc(cdt, cdn);
		if (d.barcode) {
			dataent.call({
				method: "epaas.stock.get_item_details.get_item_code",
				args: {"barcode": d.barcode },
				callback: function(r) {
					if (!r.exe){
						dataent.model.set_value(cdt, cdn, "item_code", r.message);
					}
				}
			});
		}
	},
	set_amount_quantity: function(doc, cdt, cdn) {
		var d = dataent.model.get_doc(cdt, cdn);
		if (d.qty & d.valuation_rate) {
			dataent.model.set_value(cdt, cdn, "amount", flt(d.qty) * flt(d.valuation_rate));
			dataent.model.set_value(cdt, cdn, "quantity_difference", flt(d.qty) - flt(d.current_qty));
			dataent.model.set_value(cdt, cdn, "amount_difference", flt(d.amount) - flt(d.current_amount));
		}
	},
	company: function(frm) {
		frm.trigger("toggle_display_account_head");
	},
	toggle_display_account_head: function(frm) {
		frm.toggle_display(['expense_account', 'cost_center'],
			epaas.is_perpetual_inventory_enabled(frm.doc.company));
	},
	purpose: function(frm) {
		frm.trigger("set_expense_account");
	},
	set_expense_account: function(frm) {
		if (frm.doc.company && epaas.is_perpetual_inventory_enabled(frm.doc.company)) {
			return frm.call({
				method: "epaas.stock.doctype.stock_reconciliation.stock_reconciliation.get_difference_account",
				args: {
					"purpose": frm.doc.purpose,
					"company": frm.doc.company
				},
				callback: function(r) {
					if (!r.exc) {
						frm.set_value("expense_account", r.message);
					}
				}
			});
		}
	}
});

dataent.ui.form.on("Stock Reconciliation Item", {
	barcode: function(frm, cdt, cdn) {
		frm.events.set_item_code(frm, cdt, cdn);
	},
	warehouse: function(frm, cdt, cdn) {
		frm.events.set_valuation_rate_and_qty(frm, cdt, cdn);
	},
	item_code: function(frm, cdt, cdn) {
		frm.events.set_valuation_rate_and_qty(frm, cdt, cdn);
	},
	qty: function(frm, cdt, cdn) {
		frm.events.set_amount_quantity(frm, cdt, cdn);
	},
	valuation_rate: function(frm, cdt, cdn) {
		frm.events.set_amount_quantity(frm, cdt, cdn);
	}

});

epaas.stock.StockReconciliation = epaas.stock.StockController.extend({
	setup: function() {
		var me = this;

		this.setup_posting_date_time_check();

		if (me.frm.doc.company && epaas.is_perpetual_inventory_enabled(me.frm.doc.company)) {
			this.frm.add_fetch("company", "cost_center", "cost_center");
		}
		this.frm.fields_dict["expense_account"].get_query = function() {
			if(epaas.is_perpetual_inventory_enabled(me.frm.doc.company)) {
				return {
					"filters": {
						'company': me.frm.doc.company,
						"is_group": 0
					}
				}
			}
		}
		this.frm.fields_dict["cost_center"].get_query = function() {
			if(epaas.is_perpetual_inventory_enabled(me.frm.doc.company)) {
				return {
					"filters": {
						'company': me.frm.doc.company,
						"is_group": 0
					}
				}
			}
		}
	},

	refresh: function() {
		if(this.frm.doc.docstatus==1) {
			this.show_stock_ledger();
			if (epaas.is_perpetual_inventory_enabled(this.frm.doc.company)) {
				this.show_general_ledger();
			}
		}
	},

});

cur_frm.cscript = new epaas.stock.StockReconciliation({frm: cur_frm});