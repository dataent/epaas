// Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

dataent.provide("epaas.stock");

epaas.stock.StockController = dataent.ui.form.Controller.extend({
	onload: function() {
		// warehouse query if company
		if (this.frm.fields_dict.company) {
			this.setup_warehouse_query();
		}
	},

	setup_warehouse_query: function() {
		var me = this;
		epaas.queries.setup_queries(this.frm, "Warehouse", function() {
			return epaas.queries.warehouse(me.frm.doc);
		});
	},

	setup_posting_date_time_check: function() {
		// make posting date default and read only unless explictly checked
		dataent.ui.form.on(this.frm.doctype, 'set_posting_date_and_time_read_only', function(frm) {
			if(frm.doc.docstatus == 0 && frm.doc.set_posting_time) {
				frm.set_df_property('posting_date', 'read_only', 0);
				frm.set_df_property('posting_time', 'read_only', 0);
			} else {
				frm.set_df_property('posting_date', 'read_only', 1);
				frm.set_df_property('posting_time', 'read_only', 1);
			}
		})

		dataent.ui.form.on(this.frm.doctype, 'set_posting_time', function(frm) {
			frm.trigger('set_posting_date_and_time_read_only');
		});

		dataent.ui.form.on(this.frm.doctype, 'refresh', function(frm) {
			// set default posting date / time
			if(frm.doc.docstatus==0) {
				if(!frm.doc.posting_date) {
					frm.set_value('posting_date', dataent.datetime.nowdate());
				}
				if(!frm.doc.posting_time) {
					frm.set_value('posting_time', dataent.datetime.now_time());
				}
				frm.trigger('set_posting_date_and_time_read_only');
			}
		});
	},

	show_stock_ledger: function() {
		var me = this;
		if(this.frm.doc.docstatus===1) {
			cur_frm.add_custom_button(__("Stock Ledger"), function() {
				dataent.route_options = {
					voucher_no: me.frm.doc.name,
					from_date: me.frm.doc.posting_date,
					to_date: me.frm.doc.posting_date,
					company: me.frm.doc.company
				};
				dataent.set_route("query-report", "Stock Ledger");
			}, __("View"));
		}

	},

	show_general_ledger: function() {
		var me = this;
		if(this.frm.doc.docstatus===1) {
			cur_frm.add_custom_button(__('Accounting Ledger'), function() {
				dataent.route_options = {
					voucher_no: me.frm.doc.name,
					from_date: me.frm.doc.posting_date,
					to_date: me.frm.doc.posting_date,
					company: me.frm.doc.company,
					group_by: "Group by Voucher (Consolidated)"
				};
				dataent.set_route("query-report", "General Ledger");
			}, __("View"));
		}
	}
});
