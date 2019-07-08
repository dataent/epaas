// Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

dataent.ui.form.on("Campaign", "refresh", function(frm) {
	epaas.toggle_naming_series();
	if(frm.doc.__islocal) {
		frm.toggle_display("naming_series", dataent.boot.sysdefaults.campaign_naming_by=="Naming Series");
	}
	else{
		cur_frm.add_custom_button(__("View Leads"), function() {
			dataent.route_options = {"source": "Campaign","campaign_name": frm.doc.name}
			dataent.set_route("List", "Lead");
		}, "fa fa-list", true);
	}
})
