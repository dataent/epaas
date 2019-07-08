// Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt
dataent.ui.form.on("Project", {
	setup: function (frm) {
		frm.set_indicator_formatter('title',
			function (doc) {
				let indicator = 'orange';
				if (doc.status == 'Overdue') {
					indicator = 'red';
				} else if (doc.status == 'Cancelled') {
					indicator = 'dark grey';
				} else if (doc.status == 'Closed') {
					indicator = 'green';
				}
				return indicator;
			}
		);
	},

	onload: function (frm) {
		var so = dataent.meta.get_docfield("Project", "sales_order");
		so.get_route_options_for_new_doc = function (field) {
			if (frm.is_new()) return;
			return {
				"customer": frm.doc.customer,
				"project_name": frm.doc.name
			}
		}

		frm.set_query('customer', 'epaas.controllers.queries.customer_query');

		frm.set_query("user", "users", function () {
			return {
				query: "epaas.projects.doctype.project.project.get_users_for_project"
			}
		});

		// sales order
		frm.set_query('sales_order', function () {
			var filters = {
				'project': ["in", frm.doc.__islocal ? [""] : [frm.doc.name, ""]]
			};

			if (frm.doc.customer) {
				filters["customer"] = frm.doc.customer;
			}

			return {
				filters: filters
			}
		});

		if (dataent.model.can_read("Task")) {
			frm.add_custom_button(__("Gantt Chart"), function () {
				dataent.route_options = {
					"project": frm.doc.name
				};
				dataent.set_route("List", "Task", "Gantt");
			});

			frm.add_custom_button(__("Kanban Board"), () => {
				dataent.call('epaas.projects.doctype.project.project.create_kanban_board_if_not_exists', {
					project: frm.doc.project_name
				}).then(() => {
					dataent.set_route('List', 'Task', 'Kanban', frm.doc.project_name);
				});
			});
		}
	},

	refresh: function (frm) {
		if (frm.doc.__islocal) {
			frm.web_link && frm.web_link.remove();
		} else {
			frm.add_web_link("/projects?project=" + encodeURIComponent(frm.doc.name));

			frm.trigger('show_dashboard');
		}
	},
	tasks_refresh: function (frm) {
		var grid = frm.get_field('tasks').grid;
		grid.wrapper.find('select[data-fieldname="status"]').each(function () {
			if ($(this).val() === 'Open') {
				$(this).addClass('input-indicator-open');
			} else {
				$(this).removeClass('input-indicator-open');
			}
		});
	},
});

dataent.ui.form.on("Project Task", {
	edit_task: function(frm, doctype, name) {
		var doc = dataent.get_doc(doctype, name);
		if(doc.task_id) {
			dataent.set_route("Form", "Task", doc.task_id);
		} else {
			dataent.msgprint(__("Save the document first."));
		}
	},

	edit_timesheet: function(frm, cdt, cdn) {
		var child = locals[cdt][cdn];
		dataent.route_options = {"project": frm.doc.project_name, "task": child.task_id};
		dataent.set_route("List", "Timesheet");
	},

	make_timesheet: function(frm, cdt, cdn) {
		var child = locals[cdt][cdn];
		dataent.model.with_doctype('Timesheet', function() {
			var doc = dataent.model.get_new_doc('Timesheet');
			var row = dataent.model.add_child(doc, 'time_logs');
			row.project = frm.doc.project_name;
			row.task = child.task_id;
			dataent.set_route('Form', doc.doctype, doc.name);
		})
	},

	status: function(frm, doctype, name) {
		frm.trigger('tasks_refresh');
	},
});
