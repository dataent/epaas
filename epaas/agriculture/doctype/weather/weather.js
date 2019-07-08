// Copyright (c) 2017, Dataent Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

dataent.ui.form.on('Weather', {
	onload: (frm) => {
		if (frm.doc.weather_parameter == undefined) frm.call('load_contents');
	}
});
