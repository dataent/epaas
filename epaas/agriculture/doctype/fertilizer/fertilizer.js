// Copyright (c) 2017, Dataent Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

dataent.ui.form.on('Fertilizer', {
	onload: (frm) => {
		if (frm.doc.fertilizer_contents == undefined) frm.call('load_contents');
	}
});
