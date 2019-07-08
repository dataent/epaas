dataent.ui.form.on("Room", "refresh", function(frm) {
	if(!cur_frm.doc.__islocal) {
		frm.add_custom_button(__("Course Schedule"), function() {
			dataent.route_options = {
				room: frm.doc.name
			}
			dataent.set_route("List", "Course Schedule");
		});
	}
});