// Copyright (c) 2016, Dataent Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

dataent.ui.form.on('Student Admission', {
	program: function(frm) {
		if (frm.doc.academic_year && frm.doc.program) {
			frm.doc.route = dataent.model.scrub(frm.doc.program) + "-" + dataent.model.scrub(frm.doc.academic_year)
			frm.refresh_field("route");
		}
	},

	academic_year: function(frm) {
		frm.trigger("program");
	}
});
