// Copyright (c) 2017, Dataent Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

dataent.ui.form.on('BOM Update Tool', {
	setup: function(frm) {
		frm.set_query("current_bom", function() {
			return {
				query: "epaas.controllers.queries.bom",
				filters: {name: "!" + frm.doc.new_bom}
			};
		});

		frm.set_query("new_bom", function() {
			return {
				query: "epaas.controllers.queries.bom",
				filters: {name: "!" + frm.doc.current_bom}
			};
		});
	},

	refresh: function(frm) {
		frm.disable_save();
	},

	replace: function(frm) {
		if (frm.doc.current_bom && frm.doc.new_bom) {
			dataent.call({
				method: "epaas.manufacturing.doctype.bom_update_tool.bom_update_tool.enqueue_replace_bom",
				freeze: true,
				args: {
					args: {
						"current_bom": frm.doc.current_bom,
						"new_bom": frm.doc.new_bom
					}
				}
			});
		}
	},

	update_latest_price_in_all_boms: function() {
		dataent.call({
			method: "epaas.manufacturing.doctype.bom_update_tool.bom_update_tool.enqueue_update_cost",
			freeze: true,
			callback: function() {
				dataent.msgprint(__("Latest price updated in all BOMs"));
			}
		});
	}
});