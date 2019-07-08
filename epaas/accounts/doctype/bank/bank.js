// Copyright (c) 2018, Dataent Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

dataent.ui.form.on('Bank', {
	onload: function(frm) {
		add_fields_to_mapping_table(frm);
	},
	refresh: function(frm) {
		add_fields_to_mapping_table(frm);
	}
});


let add_fields_to_mapping_table = function (frm) {
	let options = [];

	dataent.model.with_doctype("Bank Transaction", function() {
		let meta = dataent.get_meta("Bank Transaction");
		meta.fields.forEach(value => {
			if (!["Section Break", "Column Break"].includes(value.fieldtype)) {
				options.push(value.fieldname);
			}
		});
	});

	dataent.meta.get_docfield("Bank Transaction Mapping", "bank_transaction_field",
		frm.doc.name).options = options;

	frm.fields_dict.bank_transaction_mapping.grid.refresh();
};