// Copyright (c) 2017, Dataent Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

dataent.ui.form.on('Asset Maintenance', {
	setup: (frm) => {
		frm.set_query("assign_to", "asset_maintenance_tasks", function(doc) {
			return {
				query: "epaas.assets.doctype.asset_maintenance.asset_maintenance.get_team_members",
				filters: {
					maintenance_team: doc.maintenance_team
				}
			};
		});

		frm.set_indicator_formatter('maintenance_status',
			function(doc) {
				let indicator = 'blue';
				if (doc.maintenance_status == 'Overdue') {
					indicator = 'orange';
				}
				if (doc.maintenance_status == 'Cancelled') {
					indicator = 'red';
				}
				return indicator;
			}
		);

		frm.set_query('select_serial_no', function(doc){
			return {
				asset: frm.doc.asset_name
			}
		})
	},

	select_serial_no: (frm) => {
		let serial_nos = frm.doc.serial_no || frm.doc.select_serial_no;
		if (serial_nos) {
			serial_nos = serial_nos.split('\n');
			serial_nos.push(frm.doc.select_serial_no);

			const unique_sn = serial_nos.filter(function(elem, index, self) {
			    return index === self.indexOf(elem);
			});

			frm.set_value("serial_no", unique_sn.join('\n'));
		}
	},

	refresh: (frm) => {
		if(!frm.is_new()) {
			frm.trigger('make_dashboard');
		}
	},
	make_dashboard: (frm) => {
		if(!frm.is_new()) {
			dataent.call({
				method: 'epaas.assets.doctype.asset_maintenance.asset_maintenance.get_maintenance_log',
				args: {asset_name: frm.doc.asset_name},
				callback: (r) => {
					if(!r.message) {
						return;
					}
					var section = frm.dashboard.add_section(`<h5 style="margin-top: 0px;">
						${ __("Maintenance Log") }</a></h5>`);
					var rows = $('<div></div>').appendTo(section);
					// show
					(r.message || []).forEach(function(d) {
						$(`<div class='row' style='margin-bottom: 10px;'>
							<div class='col-sm-3 small'>
								<a onclick="dataent.set_route('List', 'Asset Maintenance Log', 
									{'asset_name': '${d.asset_name}','maintenance_status': '${d.maintenance_status}' });">
									${d.maintenance_status} <span class="badge">${d.count}</span>
								</a>
							</div>
						</div>`).appendTo(rows);
					});
					frm.dashboard.show();
				}
			});
		}
	}
});

dataent.ui.form.on('Asset Maintenance Task', {
	start_date: (frm, cdt, cdn)  => {
		get_next_due_date(frm, cdt, cdn);
	},
	periodicity: (frm, cdt, cdn)  => {
		get_next_due_date(frm, cdt, cdn);
	},
	last_completion_date: (frm, cdt, cdn)  => {
		get_next_due_date(frm, cdt, cdn);
	},
	end_date: (frm, cdt, cdn)  => {
		get_next_due_date(frm, cdt, cdn);
	},
	assign_to: (frm, cdt, cdn)  => {
		var d = locals[cdt][cdn];
		if (frm.doc.__islocal) {
			dataent.model.set_value(cdt, cdn, "assign_to", "");
			dataent.model.set_value(cdt, cdn, "assign_to_name", "");
			dataent.throw(__("Please save before assigning task."));
		}
		if (d.assign_to) {
			return dataent.call({
				method: 'epaas.assets.doctype.asset_maintenance.asset_maintenance.assign_tasks',
				args: {
					asset_maintenance_name: frm.doc.name,
					assign_to_member: d.assign_to,
					maintenance_task: d.maintenance_task,
					next_due_date: d.next_due_date
				}
			});
		}
	}
});

var get_next_due_date = function (frm, cdt, cdn) {
	var d = locals[cdt][cdn];
	if (d.start_date && d.periodicity) {
		return dataent.call({
			method: 'epaas.assets.doctype.asset_maintenance.asset_maintenance.calculate_next_due_date',
			args: {
				start_date: d.start_date,
				periodicity: d.periodicity,
				end_date: d.end_date,
				last_completion_date: d.last_completion_date,
				next_due_date: d.next_due_date
			},
			callback: function(r) {
				if (r.message) {
					dataent.model.set_value(cdt, cdn, "next_due_date", r.message);
				}
				else {
					dataent.model.set_value(cdt, cdn, "next_due_date", "");
				}
			}
		});
	}
};