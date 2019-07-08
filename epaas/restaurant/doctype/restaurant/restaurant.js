// Copyright (c) 2017, Dataent Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

dataent.ui.form.on('Restaurant', {
	refresh: function(frm) {
		frm.add_custom_button(__('Order Entry'), () => {
			dataent.set_route('Form', 'Restaurant Order Entry');
		});
	}
});
