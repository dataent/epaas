// Copyright (c) 2016, Dataent Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
dataent.provide("education");

dataent.ui.form.on('Student Attendance Tool', {
	onload: function(frm) {
		frm.set_query("student_group", function() {
			return {
				"filters": {
					"group_based_on": frm.doc.group_based_on,
					"disabled": 0
				}
			};
		});
	},

	refresh: function(frm) {
		if (dataent.route_options) {
			frm.set_value("based_on", dataent.route_options.based_on);
			frm.set_value("student_group", dataent.route_options.student_group);
			frm.set_value("course_schedule", dataent.route_options.course_schedule);
			dataent.route_options = null;
		}
		frm.disable_save();
	},

	based_on: function(frm) {
		if (frm.doc.based_on == "Student Group") {
			frm.set_value("course_schedule", "");
		} else {
			frm.set_value("student_group", "");
		}
	},

	student_group: function(frm) {
		if ((frm.doc.student_group && frm.doc.date) || frm.doc.course_schedule) {
			var method = "epaas.education.doctype.student_attendance_tool.student_attendance_tool.get_student_attendance_records";

			dataent.call({
				method: method,
				args: {
					based_on: frm.doc.based_on,
					student_group: frm.doc.student_group,
					date: frm.doc.date,
					course_schedule: frm.doc.course_schedule
				},
				callback: function(r) {
					frm.events.get_students(frm, r.message);
				}
			})
		}
	},

	date: function(frm) {
		frm.trigger("student_group");
	},

	course_schedule: function(frm) {
		frm.trigger("student_group");
	},

	get_students: function(frm, students) {
		if (!frm.students_area) {
			frm.students_area = $('<div>')
				.appendTo(frm.fields_dict.students_html.wrapper);
		}
		students = students || [];
		frm.students_editor = new education.StudentsEditor(frm, frm.students_area, students);
	}
});


education.StudentsEditor = Class.extend({
	init: function(frm, wrapper, students) {
		this.wrapper = wrapper;
		this.frm = frm;
		if(students.length > 0) {
			this.make(frm, students);
		} else {
			this.show_empty_state();
		}
	},
	make: function(frm, students) {
		var me = this;

		$(this.wrapper).empty();
		var student_toolbar = $('<p>\
			<button class="btn btn-default btn-add btn-xs" style="margin-right: 5px;"></button>\
			<button class="btn btn-xs btn-default btn-remove" style="margin-right: 5px;"></button>\
			<button class="btn btn-default btn-primary btn-mark-att btn-xs"></button></p>').appendTo($(this.wrapper));

		student_toolbar.find(".btn-add")
			.html(__('Check all'))
			.on("click", function() {
				$(me.wrapper).find('input[type="checkbox"]').each(function(i, check) {
					if (!$(check).prop("disabled")) {
						check.checked = true;
					}
				});
			});

		student_toolbar.find(".btn-remove")
			.html(__('Uncheck all'))
			.on("click", function() {
				$(me.wrapper).find('input[type="checkbox"]').each(function(i, check) {
					if (!$(check).prop("disabled")) {
						check.checked = false;
					}
				});
			});

		student_toolbar.find(".btn-mark-att")
			.html(__('Mark Attendance'))
			.on("click", function() {
				$(me.wrapper.find(".btn-mark-att")).attr("disabled", true);
				var studs = [];
				$(me.wrapper.find('input[type="checkbox"]')).each(function(i, check) {
					var $check = $(check);
					studs.push({
						student: $check.data().student,
						student_name: $check.data().studentName,
						group_roll_number: $check.data().group_roll_number,
						disabled: $check.prop("disabled"),
						checked: $check.is(":checked")
					});
				});

				var students_present = studs.filter(function(stud) {
					return !stud.disabled && stud.checked;
				});

				var students_absent = studs.filter(function(stud) {
					return !stud.disabled && !stud.checked;
				});

				dataent.confirm(__("Do you want to update attendance?<br>Present: {0}\
					<br>Absent: {1}", [students_present.length, students_absent.length]),
					function() {	//ifyes
						if(!dataent.request.ajax_count) {
							dataent.call({
								method: "epaas.education.api.mark_attendance",
								freeze: true,
								freeze_message: "Marking attendance",
								args: {
									"students_present": students_present,
									"students_absent": students_absent,
									"student_group": frm.doc.student_group,
									"course_schedule": frm.doc.course_schedule,
									"date": frm.doc.date
								},
								callback: function(r) {
									$(me.wrapper.find(".btn-mark-att")).attr("disabled", false);
									frm.trigger("student_group");
								}
							});
						}
					},
					function() {	//ifno
						$(me.wrapper.find(".btn-mark-att")).attr("disabled", false);
					}
				);
			});

		var htmls = students.map(function(student) {
			return dataent.render_template("student_button", {
				student: student.student,
				student_name: student.student_name,
				group_roll_number: student.group_roll_number,
				status: student.status
			})
		});

		$(htmls.join("")).appendTo(me.wrapper);
	},

	show_empty_state: function() {
		$(this.wrapper).html(
			`<div class="text-center text-muted" style="line-height: 100px;">
				${__("No Students in")} ${this.frm.doc.student_group}
			</div>`
		);
	}
});