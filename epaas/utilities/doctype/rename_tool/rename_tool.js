// Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt


dataent.ui.form.on("Rename Tool", {
	onload: function(frm) {
		return dataent.call({
			method: "epaas.utilities.doctype.rename_tool.rename_tool.get_doctypes",
			callback: function(r) {
				frm.set_df_property("select_doctype", "options", r.message);
			}
		});
	},
	refresh: function(frm) {
		frm.disable_save();
		if (!frm.doc.file_to_rename) {
			frm.get_field("rename_log").$wrapper.html("");
		}
		frm.page.set_primary_action(__("Rename"), function() {
			frm.get_field("rename_log").$wrapper.html("<p>Renaming...</p>");
			dataent.call({
				method: "epaas.utilities.doctype.rename_tool.rename_tool.upload",
				args: {
					select_doctype: frm.doc.select_doctype
				},
				callback: function(r) {
					frm.get_field("rename_log").$wrapper.html(r.message.join("<br>"));
				}
			});
		});
	}
})
