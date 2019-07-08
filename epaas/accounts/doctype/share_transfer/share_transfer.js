// Copyright (c) 2017, Dataent Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

dataent.provide("epaas.share_transfer");

dataent.ui.form.on('Share Transfer', {
	refresh: function(frm) {
		// Don't show Parties which are a Company
		let shareholders = ['from_shareholder', 'to_shareholder'];
		shareholders.forEach((shareholder) => {
			frm.fields_dict[shareholder].get_query = function() {
				return {
					filters: [
						["Shareholder", "is_company", "=", 0]
					]
				};
			};
		});
		if (frm.doc.docstatus == 1) {
			frm.add_custom_button(__('Make Journal Entry'), function () {
				epaas.share_transfer.make_jv(frm);
			});
		}
	},
	no_of_shares: (frm) => {
		if (frm.doc.rate != undefined || frm.doc.rate != null){
			epaas.share_transfer.update_amount(frm);
		}
	},
	rate: (frm) => {
		if (frm.doc.no_of_shares != undefined || frm.doc.no_of_shares != null){
			epaas.share_transfer.update_amount(frm);
		}
	},
	company: async function(frm) {
		if (frm.doc.company) {
			let currency = (await dataent.db.get_value("Company", frm.doc.company, "default_currency")).message.default_currency;
			frm.set_query("equity_or_liability_account", function() {
				return {
					filters: {
						"is_group":0,
						"root_type": ["in",["Equity","Liability"]],
						"company": frm.doc.company,
						"account_currency": currency
					}
				};
			});
			frm.set_query("asset_account", function() {
				return {
					filters: {
						"is_group":0,
						"root_type":"Asset",
						"company": frm.doc.company,
						"account_currency": currency
					}
				};
			});
		}
	}
});

epaas.share_transfer.update_amount = function(frm) {
	frm.doc.amount = frm.doc.no_of_shares * frm.doc.rate;
	frm.refresh_field("amount");
};

epaas.share_transfer.make_jv = function (frm) {
	var account, payment_account, credit_applicant_type, credit_applicant,
		debit_applicant_type, debit_applicant;

	if (frm.doc.transfer_type == "Transfer") {
		account = frm.doc.equity_or_liability_account;
		payment_account = frm.doc.equity_or_liability_account;
		credit_applicant_type = "Shareholder";
		credit_applicant = frm.doc.to_shareholder;
		debit_applicant_type = "Shareholder";
		debit_applicant = frm.doc.from_shareholder;
	}
	else if (frm.doc.transfer_type == "Issue") {
		account = frm.doc.asset_account;
		payment_account = frm.doc.equity_or_liability_account;
		credit_applicant_type = "Shareholder";
		credit_applicant = frm.doc.to_shareholder;
		debit_applicant_type = "";
		debit_applicant = "";
	}
	else {
		account = frm.doc.equity_or_liability_account;
		payment_account = frm.doc.asset_account;
		credit_applicant_type = "";
		credit_applicant = "";
		debit_applicant_type = "Shareholder";
		debit_applicant = frm.doc.from_shareholder;
	}
	dataent.call({
		args: {
			"company": frm.doc.company,
			"account": account,
			"amount": frm.doc.amount,
			"payment_account": payment_account,
			"credit_applicant_type": credit_applicant_type,
			"credit_applicant": credit_applicant,
			"debit_applicant_type": debit_applicant_type,
			"debit_applicant": debit_applicant
		},
		method: "epaas.accounts.doctype.share_transfer.share_transfer.make_jv_entry",
		callback: function (r) {
			var doc = dataent.model.sync(r.message)[0];
			dataent.set_route("Form", doc.doctype, doc.name);
		}
	});
};