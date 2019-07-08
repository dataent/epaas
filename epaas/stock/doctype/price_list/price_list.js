// Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

dataent.ui.form.on("Price List", {
	refresh: function(frm) {
		let me = this;
		frm.add_custom_button(__("Add / Edit Prices"), function() {
			dataent.route_options = {
				"price_list": frm.doc.name
			};
			dataent.set_route("Report", "Item Price");
		}, "fa fa-money");
	}
});