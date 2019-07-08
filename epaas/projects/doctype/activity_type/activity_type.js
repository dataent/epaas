dataent.ui.form.on("Activity Type", {
	refresh: function(frm) {
		frm.add_custom_button(__("Activity Cost per Employee"), function() {
			dataent.route_options = {"activity_type": frm.doc.name};
			dataent.set_route("List", "Activity Cost");
		});
	}
});
