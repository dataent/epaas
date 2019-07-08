// Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

dataent.ui.form.on("Workstation", {
	onload: function(frm) {
		if(frm.is_new())
		{
			dataent.call({
				type:"GET",
				method:"epaas.manufacturing.doctype.workstation.workstation.get_default_holiday_list",
				callback: function(r) {
					if(!r.exe && r.message){
						cur_frm.set_value("holiday_list", r.message);
					}
				}
			})
		}
	}
})