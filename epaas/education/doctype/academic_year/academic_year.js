dataent.ui.form.on("Academic Year", "refresh", function(frm) {
	if(!frm.doc.__islocal) {
		frm.add_custom_button(__("Student Group"), function() {
			dataent.route_options = {
				academic_year: frm.doc.name
			}
			dataent.set_route("List", "Student Group");
		});
	}
});