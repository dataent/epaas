// Copyright (c) 2018, Dataent Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

dataent.ui.form.on('Marketplace Settings', {
	refresh: function(frm) {
		$('#toolbar-user .marketplace-link').toggle(!frm.doc.disable_marketplace);
	},
});
