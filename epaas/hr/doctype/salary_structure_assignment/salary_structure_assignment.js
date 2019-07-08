// Copyright (c) 2018, Dataent Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

dataent.ui.form.on('Salary Structure Assignment', {
	setup: function(frm) {
		frm.set_query("employee", function() {
			return {
				query: "epaas.controllers.queries.employee_query",
				filters: {
					company: frm.doc.company
				}
			}
		});
		frm.set_query("salary_structure", function() {
			return {
				filters: {
					company: frm.doc.company,
					docstatus: 1,
					is_active: "Yes"
				}
			}
		});
	},
	employee: function(frm) {
		if(frm.doc.employee){
			dataent.call({
				method: "dataent.client.get_value",
				args:{
					doctype: "Employee",
					fieldname: "company",
					filters:{
						name: frm.doc.employee
					}
				},
				callback: function(data) {
					if(data.message){
						frm.set_value("company", data.message.company);
					}
				}
			});
		}
		else{
			frm.set_value("company", null);
		}
	}
});
