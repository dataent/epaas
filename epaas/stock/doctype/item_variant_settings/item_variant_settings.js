// Copyright (c) 2017, Dataent Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

dataent.ui.form.on('Item Variant Settings', {
	setup: function(frm) {
		const allow_fields = [];
		const exclude_fields = ["naming_series", "item_code", "item_name", "show_in_website",
		"show_variant_in_website", "opening_stock", "variant_of", "valuation_rate"];

		dataent.model.with_doctype('Item', () => {
			dataent.get_meta('Item').fields.forEach(d => {
				if(!in_list(['HTML', 'Section Break', 'Column Break', 'Button', 'Read Only'], d.fieldtype)
					&& !d.no_copy && !in_list(exclude_fields, d.fieldname)) {
					allow_fields.push(d.fieldname);
				}
			});

			const child = dataent.meta.get_docfield("Variant Field", "field_name", frm.doc.name);
			child.options = allow_fields;
		});
	}
});
