dataent.provide("education");

cur_frm.add_fetch("student_group", "course", "course")
dataent.ui.form.on("Course Schedule", {
	refresh: function(frm) {
		if (!frm.doc.__islocal) {
			frm.add_custom_button(__("Attendance"), function() {
				dataent.route_options = {
					based_on: "Course Schedule",
					course_schedule: frm.doc.name
				}
				dataent.set_route("Form", "Student Attendance Tool");
			});
		}
	}
});