cur_frm.add_fetch("employee", "department", "department");
cur_frm.add_fetch("employee", "image", "image");

dataent.ui.form.on("Instructor", {
	employee: function(frm) {
		if(!frm.doc.employee) return;
		dataent.db.get_value('Employee', {name: frm.doc.employee}, 'company', (company) => {
			frm.set_query("department", function() {
				return {
					"filters": {
						"company": company,
					}
				};
			});

			frm.set_query("department", "instructor_log", function() {
				return {
					"filters": {
						"company": company,
					}
				};
			});
		});
	},
	refresh: function(frm) {
		if(!frm.doc.__islocal) {
			frm.add_custom_button(__("Student Group"), function() {
				dataent.route_options = {
					instructor: frm.doc.name
				}
				dataent.set_route("List", "Student Group");
			});
			frm.add_custom_button(__("Course Schedule"), function() {
				dataent.route_options = {
					instructor: frm.doc.name
				}
				dataent.set_route("List", "Course Schedule");
			});
			frm.add_custom_button(__("As Examiner"), function() {
				dataent.route_options = {
					examiner: frm.doc.name
				}
				dataent.set_route("List", "Assessment Plan");
			}, __("Assessment Plan"));
			frm.add_custom_button(__("As Supervisor"), function() {
				dataent.route_options = {
					supervisor: frm.doc.name
				}
				dataent.set_route("List", "Assessment Plan");
			}, __("Assessment Plan"));
		}
	}
});
