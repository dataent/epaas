cur_frm.add_fetch("student", "title", "student_name");

dataent.ui.form.on("Student Group", {
	onload: function(frm) {
		frm.set_query("academic_term", function() {
			return {
				"filters": {
					"academic_year": (frm.doc.academic_year)
				}
			};
		});
		if (!frm.__islocal) {
			frm.set_query("student", "students", function() {
				return{
					query: "epaas.education.doctype.student_group.student_group.fetch_students",
					filters: {
						'academic_year': frm.doc.academic_year,
						'group_based_on': frm.doc.group_based_on,
						'academic_term': frm.doc.academic_term,
						'program': frm.doc.program,
						'batch': frm.doc.batch,
						'course': frm.doc.course,
						'student_group': frm.doc.name
					}
				}
			});
		}
	},

	refresh: function(frm) {
		if (!frm.doc.__islocal) {
			frm.add_custom_button(__("Attendance"), function() {
				dataent.route_options = {
					based_on: "Student Group",
					student_group: frm.doc.name
				}
				dataent.set_route("List", "Student Attendance Tool");
			});
			frm.add_custom_button(__("Course Schedule"), function() {
				dataent.route_options = {
					student_group: frm.doc.name
				}
				dataent.set_route("List", "Course Schedule");
			});
			frm.add_custom_button(__("Assessment Plan"), function() {
				dataent.route_options = {
					student_group: frm.doc.name
				}
				dataent.set_route("List", "Assessment Plan");
			});
			frm.add_custom_button(__("Update Email Group"), function() {
				dataent.call({
					method: "epaas.education.api.update_email_group",
					args: {
						"doctype": "Student Group",
						"name": frm.doc.name
					}
				});
			});
			frm.add_custom_button(__("Newsletter"), function() {
				dataent.route_options = {
					"Newsletter Email Group.email_group": frm.doc.name
				}
				dataent.set_route("List", "Newsletter");
			});
		}
	},
	
	group_based_on: function(frm) {
		if (frm.doc.group_based_on == "Batch") {
			frm.doc.course = null;
		}
	},

	get_students: function(frm) {
		if (frm.doc.group_based_on == "Batch" || frm.doc.group_based_on == "Course") {
			var student_list = [];
			var max_roll_no = 0;
			$.each(frm.doc.students, function(i,d) {
				student_list.push(d.student);
				if (d.group_roll_number>max_roll_no) {
					max_roll_no = d.group_roll_number;
				}
			});

			if(frm.doc.academic_year) {
				dataent.call({
					method: "epaas.education.doctype.student_group.student_group.get_students",
					args: {
						"academic_year": frm.doc.academic_year,
						"academic_term": frm.doc.academic_term,
						"group_based_on": frm.doc.group_based_on,
						"program": frm.doc.program,
						"batch" : frm.doc.batch,
						"course": frm.doc.course
					},
					callback: function(r) {
						if(r.message) {
							$.each(r.message, function(i, d) {
								if(!in_list(student_list, d.student)) {
									var s = frm.add_child("students");
									s.student = d.student;
									s.student_name = d.student_name;
									if (d.active === 0) {
										s.active = 0;
									}
									s.group_roll_number = ++max_roll_no;
								}
							});
							refresh_field("students");
							frm.save();
						} else {
							dataent.msgprint(__("Student Group is already updated."))
						}
					}
				})
			}
		} else {
			dataent.msgprint(__("Select students manually for the Activity based Group"));
		}
	}
});