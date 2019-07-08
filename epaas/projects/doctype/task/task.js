// Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

dataent.provide("epaas.projects");

cur_frm.add_fetch("project", "company", "company");

dataent.ui.form.on("Task", {
	onload: function(frm) {
		frm.set_query("task", "depends_on", function() {
			var filters = {
				name: ["!=", frm.doc.name]
			};
			if(frm.doc.project) filters["project"] = frm.doc.project;
			return {
				filters: filters
			};
		})
	},

	refresh: function(frm) {
		frm.fields_dict['parent_task'].get_query = function () {
			return {
				filters: {
					"is_group": 1,
				}
			}
		}

		if (!frm.doc.is_group) {
			if (!frm.is_new()) {
				if (dataent.model.can_read("Timesheet")) {
					frm.add_custom_button(__("Timesheet"), () => {
						dataent.route_options = { "project": frm.doc.project, "task": frm.doc.name }
						dataent.set_route("List", "Timesheet");
					}, __("View"), true);
				}

				if (dataent.model.can_read("Expense Claim")) {
					frm.add_custom_button(__("Expense Claims"), () => {
						dataent.route_options = { "project": frm.doc.project, "task": frm.doc.name }
						dataent.set_route("List", "Expense Claim");
					}, __("View"), true);
				}

				if (frm.perm[0].write) {
					if (!["Closed", "Cancelled"].includes(frm.doc.status)) {
						frm.add_custom_button(__("Close"), () => {
							frm.set_value("status", "Closed");
							frm.save();
						});
					} else {
						frm.add_custom_button(__("Reopen"), () => {
							frm.set_value("status", "Open");
							frm.save();
						});
					}
				}
			}
		}
	},

	setup: function(frm) {
		frm.fields_dict.project.get_query = function() {
			return {
				query: "epaas.projects.doctype.task.task.get_project"
			}
		};
	},

	project: function(frm) {
		if(frm.doc.project) {
			return get_server_fields('get_project_details', '','', frm.doc, frm.doc.doctype,
				frm.doc.name, 1);
		}
	},

	is_group: function (frm) {
		dataent.call({
			method: "epaas.projects.doctype.task.task.check_if_child_exists",
			args: {
				name: frm.doc.name
			},
			callback: function (r) {
				if (r.message.length > 0) {
					dataent.msgprint(__(`Cannot convert it to non-group. The following child Tasks exist: ${r.message.join(", ")}.`));
					frm.reload_doc();
				}
			}
		})
	},

	validate: function(frm) {
		frm.doc.project && dataent.model.remove_from_locals("Project",
			frm.doc.project);
	},

});

cur_frm.add_fetch('task', 'subject', 'subject');
cur_frm.add_fetch('task', 'project', 'project');
