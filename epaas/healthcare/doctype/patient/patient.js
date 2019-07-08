// Copyright (c) 2016, ESS LLP and contributors
// For license information, please see license.txt

dataent.ui.form.on('Patient', {
	refresh: function (frm) {
		frm.set_query("patient", "patient_relation", function () {
			return {
				filters: [
					["Patient", "name", "!=", frm.doc.name]
				]
			};
		});
		if (dataent.defaults.get_default("patient_master_name") != "Naming Series") {
			frm.toggle_display("naming_series", false);
		} else {
			epaas.toggle_naming_series();
		}
		if (dataent.defaults.get_default("collect_registration_fee") && frm.doc.disabled == 1) {
			frm.add_custom_button(__('Invoice Patient Registration'), function () {
				btn_invoice_registration(frm);
			});
		}
		if (frm.doc.patient_name && dataent.user.has_role("Physician")) {
			frm.add_custom_button(__('Medical Record'), function () {
				dataent.route_options = { "patient": frm.doc.name };
				dataent.set_route("medical_record");
			},"View");
		}
		if (!frm.doc.__islocal && (dataent.user.has_role("Nursing User") || dataent.user.has_role("Physician"))) {
			frm.add_custom_button(__('Vital Signs'), function () {
				btn_create_vital_signs(frm);
			}, "Create");
			frm.add_custom_button(__('Medical Record'), function () {
				create_medical_record(frm);
			}, "Create");
			frm.add_custom_button(__('Patient Encounter'), function () {
				btn_create_encounter(frm);
			}, "Create");
		}
	},
	onload: function (frm) {
		if(!frm.doc.dob){
			$(frm.fields_dict['age_html'].wrapper).html("");
		}
		if(frm.doc.dob){
			$(frm.fields_dict['age_html'].wrapper).html("AGE : " + get_age(frm.doc.dob));
		}
	}
});

dataent.ui.form.on("Patient", "dob", function(frm) {
	if(frm.doc.dob) {
		var today = new Date();
		var birthDate = new Date(frm.doc.dob);
		if(today < birthDate){
			dataent.msgprint(__("Please select a valid Date"));
			dataent.model.set_value(frm.doctype,frm.docname, "dob", "");
		}
		else{
			var age_str = get_age(frm.doc.dob);
			$(frm.fields_dict['age_html'].wrapper).html("AGE : " + age_str);
		}
	}
	else {
		$(frm.fields_dict['age_html'].wrapper).html("");
	}
});

var create_medical_record = function (frm) {
	dataent.route_options = {
		"patient": frm.doc.name,
		"status": "Open",
		"reference_doctype": "Patient Medical Record",
		"reference_owner": frm.doc.owner
	};
	dataent.new_doc("Patient Medical Record");
};

var get_age = function (birth) {
	var ageMS = Date.parse(Date()) - Date.parse(birth);
	var age = new Date();
	age.setTime(ageMS);
	var years = age.getFullYear() - 1970;
	return years + " Year(s) " + age.getMonth() + " Month(s) " + age.getDate() + " Day(s)";
};

var btn_create_vital_signs = function (frm) {
	if (!frm.doc.name) {
		dataent.throw(__("Please save the patient first"));
	}
	dataent.route_options = {
		"patient": frm.doc.name,
	};
	dataent.new_doc("Vital Signs");
};

var btn_create_encounter = function (frm) {
	if (!frm.doc.name) {
		dataent.throw(__("Please save the patient first"));
	}
	dataent.route_options = {
		"patient": frm.doc.name,
	};
	dataent.new_doc("Patient Encounter");
};

var btn_invoice_registration = function (frm) {
	dataent.call({
		doc: frm.doc,
		method: "invoice_patient_registration",
		callback: function(data){
			if(!data.exc){
				if(data.message.invoice){
					/* dataent.show_alert(__('Sales Invoice {0} created',
					['<a href="#Form/Sales Invoice/'+data.message.invoice+'">' + data.message.invoice+ '</a>'])); */
					dataent.set_route("Form", "Sales Invoice", data.message.invoice);
				}
				cur_frm.reload_doc();
			}
		}
	});
};

dataent.ui.form.on('Patient Relation', {
	patient_relation_add: function(frm){
		frm.fields_dict['patient_relation'].grid.get_field('patient').get_query = function(doc){
			var patient_list = [];
			if(!doc.__islocal) patient_list.push(doc.name);
			$.each(doc.patient_relation, function(idx, val){
				if (val.patient) patient_list.push(val.patient);
			});
			return { filters: [['Patient', 'name', 'not in', patient_list]] };
		};
	}
});
