// Copyright (c) 2018, Dataent Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

dataent.provide("epaas.integrations");

dataent.ui.form.on('Plaid Settings', {
	link_new_account: function(frm) {
		new epaas.integrations.plaidLink(frm);
	}
});

epaas.integrations.plaidLink = class plaidLink {
	constructor(parent) {
		this.frm = parent;
		this.product = ["transactions", "auth"];
		this.plaidUrl = 'https://cdn.plaid.com/link/v2/stable/link-initialize.js';
		this.init_config();
	}

	init_config() {
		const me = this;
		dataent.xcall('epaas.epaas_integrations.doctype.plaid_settings.plaid_settings.plaid_configuration')
			.then(result => {
				if (result !== "disabled") {
					if (result.plaid_env == undefined || result.plaid_public_key == undefined) {
						dataent.throw(__("Please add valid Plaid api keys in site_config.json first"));
					}
					me.plaid_env = result.plaid_env;
					me.plaid_public_key = result.plaid_public_key;
					me.client_name = result.client_name;
					me.init_plaid();
				} else {
					dataent.throw(__("Please save your document before adding a new account"));
				}
			});
	}

	init_plaid() {
		const me = this;
		me.loadScript(me.plaidUrl)
			.then(() => {
				me.onScriptLoaded(me);
			})
			.then(() => {
				if (me.linkHandler) {
					me.linkHandler.open();
				}
			})
			.catch((error) => {
				me.onScriptError(error);
			});
	}

	loadScript(src) {
		return new Promise(function (resolve, reject) {
			if (document.querySelector('script[src="' + src + '"]')) {
				resolve();
				return;
			}
			const el = document.createElement('script');
			el.type = 'text/javascript';
			el.async = true;
			el.src = src;
			el.addEventListener('load', resolve);
			el.addEventListener('error', reject);
			el.addEventListener('abort', reject);
			document.head.appendChild(el);
		});
	}

	onScriptLoaded(me) {
		me.linkHandler = window.Plaid.create({
			clientName: me.client_name,
			env: me.plaid_env,
			key: me.plaid_public_key,
			onSuccess: me.plaid_success,
			product: me.product
		});
	}

	onScriptError(error) {
		dataent.msgprint('There was an issue loading the link-initialize.js script');
		dataent.msgprint(error);
	}

	plaid_success(token, response) {
		const me = this;

		dataent.prompt({
			fieldtype:"Link",
			options: "Company",
			label:__("Company"),
			fieldname:"company",
			reqd:1
		}, (data) => {
			me.company = data.company;
			dataent.xcall('epaas.epaas_integrations.doctype.plaid_settings.plaid_settings.add_institution', {token: token, response: response})
				.then((result) => {
					dataent.xcall('epaas.epaas_integrations.doctype.plaid_settings.plaid_settings.add_bank_accounts', {response: response,
						bank: result, company: me.company});
				})
				.then(() => {
					dataent.show_alert({message:__("Bank accounts added"), indicator:'green'});
				});
		}, __("Select a company"), __("Continue"));
	}
};