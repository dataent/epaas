// Copyright (c) 2018, Dataent Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

dataent.ui.form.on('Bank Transaction', {
	onload(frm) {
		frm.set_query('payment_document', 'payment_entries', function() {
			return {
				"filters": {
					"name": ["in", ["Payment Entry", "Journal Entry", "Sales Invoice", "Purchase Invoice", "Expense Claim"]]
				}
			};
		});
	}
});

dataent.ui.form.on('Bank Transaction Payments', {
	payment_entries_remove: function(frm, cdt, cdn) {
		update_clearance_date(frm, cdt, cdn);
	}
});

const update_clearance_date = (frm, cdt, cdn) => {
	if (frm.doc.docstatus === 1) {
		dataent.xcall('epaas.accounts.doctype.bank_transaction.bank_transaction.unclear_reference_payment',
			{doctype: cdt, docname: cdn})
			.then(e => {
				if (e == "success") {
					dataent.show_alert({message:__("Document {0} successfully uncleared", [e]), indicator:'green'});
				}
			});
	}
};