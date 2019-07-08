// Copyright (c) 2017, Dataent Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

dataent.provide("epaas.crop");

dataent.ui.form.on('Crop', {
	refresh: (frm) => {
		frm.fields_dict.materials_required.grid.set_column_disp('bom_no', false);
	}
});

dataent.ui.form.on("BOM Item", {
	item_code: (frm, cdt, cdn) => {
		epaas.crop.update_item_rate_uom(frm, cdt, cdn);
	},
	qty: (frm, cdt, cdn) => {
		epaas.crop.update_item_qty_amount(frm, cdt, cdn);
	},
	rate: (frm, cdt, cdn) => {
		epaas.crop.update_item_qty_amount(frm, cdt, cdn);
	}
});

epaas.crop.update_item_rate_uom = function(frm, cdt, cdn) {
	let material_list = ['materials_required', 'produce', 'byproducts'];
	material_list.forEach((material) => {
		frm.doc[material].forEach((item, index) => {
			if (item.name == cdn && item.item_code){
				dataent.call({
					method:'epaas.agriculture.doctype.crop.crop.get_item_details',
					args: {
						item_code: item.item_code
					},
					callback: (r) => {
						dataent.model.set_value('BOM Item', item.name, 'uom', r.message.uom);
						dataent.model.set_value('BOM Item', item.name, 'rate', r.message.rate);
					}
				});
			}
		});
	});
};

epaas.crop.update_item_qty_amount = function(frm, cdt, cdn) {
	let material_list = ['materials_required', 'produce', 'byproducts'];
	material_list.forEach((material) => {
		frm.doc[material].forEach((item, index) => {
			if (item.name == cdn){
				if (!dataent.model.get_value('BOM Item', item.name, 'qty'))
					dataent.model.set_value('BOM Item', item.name, 'qty', 1);
				dataent.model.set_value('BOM Item', item.name, 'amount', item.qty * item.rate);
			}
		});
	});
};