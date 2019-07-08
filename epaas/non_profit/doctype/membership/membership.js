// Copyright (c) 2017, Dataent Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

dataent.ui.form.on('Membership', {
	onload:function(frm) {
		frm.add_fetch('membership_type', 'amount', 'amount');
	}
});
