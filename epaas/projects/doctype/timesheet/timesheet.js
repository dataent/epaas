// Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

dataent.ui.form.on("Timesheet", {
	setup: function(frm) {
		dataent.require("/assets/epaas/js/projects/timer.js");
		frm.add_fetch('employee', 'employee_name', 'employee_name');
		frm.fields_dict.employee.get_query = function() {
			return {
				filters:{
					'status': 'Active'
				}
			};
		};

		frm.fields_dict['time_logs'].grid.get_field('task').get_query = function(frm, cdt, cdn) {
			var child = locals[cdt][cdn];
			return{
				filters: {
					'project': child.project,
					'status': ["!=", "Cancelled"]
				}
			};
		};

		frm.fields_dict['time_logs'].grid.get_field('project').get_query = function() {
			return{
				filters: {
					'company': frm.doc.company
				}
			};
		};
	},

	onload: function(frm){
		if (frm.doc.__islocal && frm.doc.time_logs) {
			calculate_time_and_amount(frm);
		}

		if (frm.is_new()) {
			set_employee_and_company(frm);
		}
	},

	refresh: function(frm) {
		if(frm.doc.docstatus==1) {
			if(frm.doc.per_billed < 100 && frm.doc.total_billable_hours && frm.doc.total_billable_hours > frm.doc.total_billed_hours){
				frm.add_custom_button(__("Make Sales Invoice"), function() { frm.trigger("make_invoice"); },
					"fa fa-file-alt");
			}

			if(!frm.doc.salary_slip && frm.doc.employee){
				frm.add_custom_button(__("Make Salary Slip"), function() { frm.trigger("make_salary_slip"); },
					"fa fa-file-alt");
			}
		}

		if (frm.doc.docstatus < 1) {

			let button = 'Start Timer';
			$.each(frm.doc.time_logs || [], function(i, row) {
				if ((row.from_time <= dataent.datetime.now_datetime()) && !row.completed) {
					button = 'Resume Timer';
				}
			});

			frm.add_custom_button(__(button), function() {
				var flag = true;
				$.each(frm.doc.time_logs || [], function(i, row) {
					// Fetch the row for which from_time is not present
					if (flag && row.activity_type && !row.from_time){
						epaas.timesheet.timer(frm, row);
						row.from_time = dataent.datetime.now_datetime();
						frm.refresh_fields("time_logs");
						frm.save();
						flag = false;
					}
					// Fetch the row for timer where activity is not completed and from_time is before now_time
					if (flag && row.from_time <= dataent.datetime.now_datetime() && !row.completed) {
						let timestamp = moment(dataent.datetime.now_datetime()).diff(moment(row.from_time),"seconds");
						epaas.timesheet.timer(frm, row, timestamp);
						flag = false;
					}
				});
				// If no activities found to start a timer, create new
				if (flag) {
					epaas.timesheet.timer(frm);
				}
			}).addClass("btn-primary");
		}
		if(frm.doc.per_billed > 0) {
			frm.fields_dict["time_logs"].grid.toggle_enable("billing_hours", false);
			frm.fields_dict["time_logs"].grid.toggle_enable("billable", false);
		}
	},

	company: function(frm) {
		dataent.db.get_value('Company', { 'company_name' : frm.doc.company }, 'standard_working_hours')
			.then(({ message }) => {
				(dataent.working_hours = message.standard_working_hours || 0);
			});
	},

	make_invoice: function(frm) {
		let dialog = new dataent.ui.Dialog({
			title: __("Select Item (optional)"),
			fields: [
				{"fieldtype": "Link", "label": __("Item Code"), "fieldname": "item_code", "options":"Item"},
				{"fieldtype": "Link", "label": __("Customer"), "fieldname": "customer", "options":"Customer"}
			]
		});

		dialog.set_primary_action(__("Make Sales Invoice"), () => {
			var args = dialog.get_values();
			if(!args) return;
			dialog.hide();
			return dataent.call({
				type: "GET",
				method: "epaas.projects.doctype.timesheet.timesheet.make_sales_invoice",
				args: {
					"source_name": frm.doc.name,
					"item_code": args.item_code,
					"customer": args.customer
				},
				freeze: true,
				callback: function(r) {
					if(!r.exc) {
						dataent.model.sync(r.message);
						dataent.set_route("Form", r.message.doctype, r.message.name);
					}
				}
			});
		});
		dialog.show();
	},

	make_salary_slip: function(frm) {
		dataent.model.open_mapped_doc({
			method: "epaas.projects.doctype.timesheet.timesheet.make_salary_slip",
			frm: frm
		});
	},
});

dataent.ui.form.on("Timesheet Detail", {
	time_logs_remove: function(frm) {
		calculate_time_and_amount(frm);
	},

	from_time: function(frm, cdt, cdn) {
		calculate_end_time(frm, cdt, cdn);
	},

	to_time: function(frm, cdt, cdn) {
		var child = locals[cdt][cdn];
		var time_diff = (moment(child.to_time).diff(moment(child.from_time),"seconds")) / ( 60 * 60 * 24);
		var std_working_hours = 0;

		if(frm._setting_hours) return;

		var hours = moment(child.to_time).diff(moment(child.from_time), "seconds") / 3600;
		std_working_hours = time_diff * dataent.working_hours;

		if (std_working_hours < hours && std_working_hours > 0) {
			dataent.model.set_value(cdt, cdn, "hours", std_working_hours);
		} else {
			dataent.model.set_value(cdt, cdn, "hours", hours);
		}
	},

	time_logs_add: function(frm) {
		var $trigger_again = $('.form-grid').find('.grid-row').find('.btn-open-row');
		$trigger_again.on('click', () => {
			$('.form-grid')
				.find('[data-fieldname="timer"]')
				.append(dataent.render_template("timesheet"));
			frm.trigger("control_timer");
		});
	},
	hours: function(frm, cdt, cdn) {
		calculate_end_time(frm, cdt, cdn);
	},

	billing_hours: function(frm, cdt, cdn) {
		calculate_billing_costing_amount(frm, cdt, cdn);
	},

	billing_rate: function(frm, cdt, cdn) {
		calculate_billing_costing_amount(frm, cdt, cdn);
	},

	costing_rate: function(frm, cdt, cdn) {
		calculate_billing_costing_amount(frm, cdt, cdn);
	},

	billable: function(frm, cdt, cdn) {
		update_billing_hours(frm, cdt, cdn);
		update_time_rates(frm, cdt, cdn);
		calculate_billing_costing_amount(frm, cdt, cdn);
	},

	activity_type: function(frm, cdt, cdn) {
		frm.script_manager.copy_from_first_row('time_logs', frm.selected_doc,
			'project');

		dataent.call({
			method: "epaas.projects.doctype.timesheet.timesheet.get_activity_cost",
			args: {
				employee: frm.doc.employee,
				activity_type: frm.selected_doc.activity_type
			},
			callback: function(r){
				if(r.message){
					dataent.model.set_value(cdt, cdn, 'billing_rate', r.message['billing_rate']);
					dataent.model.set_value(cdt, cdn, 'costing_rate', r.message['costing_rate']);
					calculate_billing_costing_amount(frm, cdt, cdn);
				}
			}
		});
	}
});

var calculate_end_time = function(frm, cdt, cdn) {
	let child = locals[cdt][cdn];

	if(!child.from_time) {
		// if from_time value is not available then set the current datetime
		dataent.model.set_value(cdt, cdn, "from_time", dataent.datetime.get_datetime_as_string());
	}

	let d = moment(child.from_time);
	if(child.hours) {
		var time_diff = (moment(child.to_time).diff(moment(child.from_time),"seconds")) / (60 * 60 * 24);
		var std_working_hours = 0;
		var hours = moment(child.to_time).diff(moment(child.from_time), "seconds") / 3600;

		std_working_hours = time_diff * dataent.working_hours;

		if (std_working_hours < hours && std_working_hours > 0) {
			dataent.model.set_value(cdt, cdn, "hours", std_working_hours);
			dataent.model.set_value(cdt, cdn, "to_time", d.add(hours, "hours").format(dataent.defaultDatetimeFormat));
		} else {
			d.add(child.hours, "hours");
			frm._setting_hours = true;
			dataent.model.set_value(cdt, cdn, "to_time",
				d.format(dataent.defaultDatetimeFormat)).then(() => {
				frm._setting_hours = false;
			});
		}
	}
};

var update_billing_hours = function(frm, cdt, cdn){
	var child = locals[cdt][cdn];
	if(!child.billable) dataent.model.set_value(cdt, cdn, 'billing_hours', 0.0);
};

var update_time_rates = function(frm, cdt, cdn){
	var child = locals[cdt][cdn];
	if(!child.billable){
		dataent.model.set_value(cdt, cdn, 'billing_rate', 0.0);
	}
};

var calculate_billing_costing_amount = function(frm, cdt, cdn){
	var child = locals[cdt][cdn];
	var billing_amount = 0.0;
	var costing_amount = 0.0;

	if(child.billing_hours && child.billable){
		billing_amount = (child.billing_hours * child.billing_rate);
	}
	costing_amount = flt(child.costing_rate * child.hours);
	dataent.model.set_value(cdt, cdn, 'billing_amount', billing_amount);
	dataent.model.set_value(cdt, cdn, 'costing_amount', costing_amount);
	calculate_time_and_amount(frm);
};

var calculate_time_and_amount = function(frm) {
	var tl = frm.doc.time_logs || [];
	var total_working_hr = 0;
	var total_billing_hr = 0;
	var total_billable_amount = 0;
	var total_costing_amount = 0;
	for(var i=0; i<tl.length; i++) {
		if (tl[i].hours) {
			total_working_hr += tl[i].hours;
			total_billable_amount += tl[i].billing_amount;
			total_costing_amount += tl[i].costing_amount;

			if(tl[i].billable){
				total_billing_hr += tl[i].billing_hours;
			}
		}
	}

	frm.set_value("total_billable_hours", total_billing_hr);
	frm.set_value("total_hours", total_working_hr);
	frm.set_value("total_billable_amount", total_billable_amount);
	frm.set_value("total_costing_amount", total_costing_amount);
};

// set employee (and company) to the one that's currently logged in
const set_employee_and_company = function(frm) {
	const options = { user_id: dataent.session.user };
	const fields = ['name', 'company'];
	dataent.db.get_value('Employee', options, fields).then(({ message }) => {
		if (message) {
			// there is an employee with the currently logged in user_id
			frm.set_value("employee", message.name);
			frm.set_value("company", message.company);
		}
	});
};
