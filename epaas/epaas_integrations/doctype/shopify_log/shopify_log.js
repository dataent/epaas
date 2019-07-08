// Copyright (c) 2016, Dataent Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

dataent.ui.form.on('Shopify Log', {
	refresh: function(frm) {
		if (frm.doc.request_data && frm.doc.status=='Error'){
			frm.add_custom_button('Resync', function() {
				dataent.call({
					method:"epaas.epaas_integrations.doctype.shopify_log.shopify_log.resync",
					args:{
						method:frm.doc.method,
						name: frm.doc.name,
						request_data: frm.doc.request_data
					},
					callback: function(r){
						dataent.msgprint(__("Order rescheduled for sync"))
					}
				})
			}).addClass('btn-primary');
		}
	}
});
