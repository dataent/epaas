// Copyright (c) 2017, Dataent Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

dataent.ui.form.on('Asset Repair', {
	repair_status: (frm) => {
		if (frm.doc.completion_date && frm.doc.repair_status == "Completed") {
			dataent.call ({
				method: "epaas.assets.doctype.asset_repair.asset_repair.get_downtime",
				args: {
					"failure_date":frm.doc.failure_date,
					"completion_date":frm.doc.completion_date
				},
				callback: function(r) {
					if(r.message) {
						frm.set_value("downtime", r.message + " Hrs");
					}
				}
			});
		}
	}
});
