// Copyright (c) 2016, ESS LLP and contributors
// For license information, please see license.txt

dataent.ui.form.on('Healthcare Practitioner', {
	setup: function(frm) {
		frm.set_query('account', 'accounts', function(doc, cdt, cdn) {
			var d	= locals[cdt][cdn];
			return {
				filters: {
					'root_type': 'Income',
					'company': d.company,
					'is_group': 0
				}
			};
		});
	},
	refresh: function(frm) {
		dataent.dynamic_link = {doc: frm.doc, fieldname: 'name', doctype: 'Healthcare Practitioner'};
		if(!frm.is_new()) {
			dataent.contacts.render_address_and_contact(frm);
		}
		frm.set_query("service_unit", "practitioner_schedules", function(){
			return {
				filters: {
					"is_group": false,
					"allow_appointments": true
				}
			};
		});
		set_query_service_item(frm, 'inpatient_visit_charge_item');
		set_query_service_item(frm, 'op_consulting_charge_item');
	}
});

var set_query_service_item = function(frm, service_item_field) {
	frm.set_query(service_item_field, function() {
		return {
			filters: {
				'is_sales_item': 1,
				'is_stock_item': 0
			}
		};
	});
};

dataent.ui.form.on("Healthcare Practitioner", "user_id",function(frm) {
	if(frm.doc.user_id){
		dataent.call({
			"method": "dataent.client.get",
			args: {
				doctype: "User",
				name: frm.doc.user_id
			},
			callback: function (data) {

				dataent.model.get_value('Employee', {'user_id': frm.doc.user_id}, 'name',
					function(data) {
						if(data){
							if(!frm.doc.employee || frm.doc.employee != data.name)
								dataent.model.set_value(frm.doctype,frm.docname, "employee", data.name);
						}else{
							dataent.model.set_value(frm.doctype,frm.docname, "employee", "");
						}
					}
				);

				if(!frm.doc.first_name || frm.doc.first_name != data.message.first_name)
					dataent.model.set_value(frm.doctype,frm.docname, "first_name", data.message.first_name);
				if(!frm.doc.middle_name || frm.doc.middle_name != data.message.middle_name)
					dataent.model.set_value(frm.doctype,frm.docname, "middle_name", data.message.middle_name);
				if(!frm.doc.last_name || frm.doc.last_name != data.message.last_name)
					dataent.model.set_value(frm.doctype,frm.docname, "last_name", data.message.last_name);
				if(!frm.doc.mobile_phone || frm.doc.mobile_phone != data.message.mobile_no)
					dataent.model.set_value(frm.doctype,frm.docname, "mobile_phone", data.message.mobile_no);
			}
		});
	}
});

dataent.ui.form.on("Healthcare Practitioner", "employee", function(frm) {
	if(frm.doc.employee){
		dataent.call({
			"method": "dataent.client.get",
			args: {
				doctype: "Employee",
				name: frm.doc.employee
			},
			callback: function (data) {
				if(!frm.doc.user_id || frm.doc.user_id != data.message.user_id)
					frm.set_value("user_id", data.message.user_id);
				if(!frm.doc.designation || frm.doc.designation != data.message.designation)
					dataent.model.set_value(frm.doctype,frm.docname, "designation", data.message.designation);
				if(!frm.doc.first_name || !frm.doc.user_id){
					dataent.model.set_value(frm.doctype,frm.docname, "first_name", data.message.employee_name);
					dataent.model.set_value(frm.doctype,frm.docname, "middle_name", "");
					dataent.model.set_value(frm.doctype,frm.docname, "last_name", "");
				}
				if(!frm.doc.mobile_phone || !frm.doc.user_id)
					dataent.model.set_value(frm.doctype,frm.docname, "mobile_phone", data.message.cell_number);
				if(!frm.doc.address || frm.doc.address != data.message.current_address)
					dataent.model.set_value(frm.doctype,frm.docname, "address", data.message.current_address);
			}
		});
	}
});
