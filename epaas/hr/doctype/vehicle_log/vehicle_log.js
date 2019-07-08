// Copyright (c) 2016, Dataent Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

dataent.ui.form.on("Vehicle Log", {
	refresh: function(frm,cdt,cdn) {
		var vehicle_log=dataent.model.get_doc(cdt,cdn);
		if (vehicle_log.license_plate) {
			dataent.call({
				method: "epaas.hr.doctype.vehicle_log.vehicle_log.get_make_model",
				args: {
					license_plate: vehicle_log.license_plate
				},
				callback: function(r) {
					dataent.model.set_value(cdt, cdn, ("model"), r.message[0]);
					dataent.model.set_value(cdt, cdn, ("make"), r.message[1]);
				}
			})
		}

		if(frm.doc.docstatus == 1) {
			frm.add_custom_button(__('Expense Claim'), function() {
				frm.events.expense_claim(frm)
			}, __("Make"));
			frm.page.set_inner_btn_group_as_primary(__("Make"));
		}
	},

	expense_claim: function(frm){
		dataent.call({
			method: "epaas.hr.doctype.vehicle_log.vehicle_log.make_expense_claim",
			args:{
				docname: frm.doc.name
			},
			callback: function(r){
				var doc = dataent.model.sync(r.message);
				dataent.set_route('Form', 'Expense Claim', r.message.name);
			}
		});
	}
});

