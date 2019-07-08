dataent.ui.form.on("Course", "refresh", function(frm) {
	if(!cur_frm.doc.__islocal) {
		frm.add_custom_button(__("Program"), function() {
			dataent.route_options = {
				"Program Course.course": frm.doc.name
			}
			dataent.set_route("List", "Program");
		});
		
		frm.add_custom_button(__("Student Group"), function() {
			dataent.route_options = {
				course: frm.doc.name
			}
			dataent.set_route("List", "Student Group");
		});
		
		frm.add_custom_button(__("Course Schedule"), function() {
			dataent.route_options = {
				course: frm.doc.name
			}
			dataent.set_route("List", "Course Schedule");
		});
		
		frm.add_custom_button(__("Assessment Plan"), function() {
			dataent.route_options = {
				course: frm.doc.name
			}
			dataent.set_route("List", "Assessment Plan");
		});
	}

	frm.set_query('default_grading_scale', function(){
		return {
			filters: {
				docstatus: 1
			}
		}
	});
});