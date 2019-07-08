dataent.provide("dataent.treeview_settings")

dataent.treeview_settings["Account"] = {
	breadcrumbs: "Accounts",
	title: __("Chart Of Accounts"),
	get_tree_root: false,
	filters: [
		{
			fieldname: "company",
			fieldtype:"Select",
			options: epaas.utils.get_tree_options("company"),
			label: __("Company"),
			default: epaas.utils.get_tree_default("company"),
			on_change: function() {
				var me = dataent.treeview_settings['Account'].treeview;
				var company = me.page.fields_dict.company.get_value();
				dataent.call({
					method: "epaas.accounts.doctype.account.account.get_root_company",
					args: {
						company: company,
					},
					callback: function(r) {
						if(r.message) {
							let root_company = r.message.length ? r.message[0] : "";
							me.page.fields_dict.root_company.set_value(root_company);

							dataent.db.get_value("Company", {"name": company}, "allow_account_creation_against_child_company", (r) => {
								dataent.flags.ignore_root_company_validation = r.allow_account_creation_against_child_company;
							});
						}
					}
				});
			}
		},
		{
			fieldname: "root_company",
			fieldtype:"Data",
			label: __("Root Company"),
			hidden: true,
			disable_onchange: true
		}
	],
	root_label: "Accounts",
	get_tree_nodes: 'epaas.accounts.utils.get_children',
	add_tree_node: 'epaas.accounts.utils.add_ac',
	menu_items:[
		{
			label: __('New Company'),
			action: function() { dataent.new_doc("Company", true) },
			condition: 'dataent.boot.user.can_create.indexOf("Company") !== -1'
		}
	],
	fields: [
		{fieldtype:'Data', fieldname:'account_name', label:__('New Account Name'), reqd:true,
			description: __("Name of new Account. Note: Please don't create accounts for Customers and Suppliers")},
		{fieldtype:'Data', fieldname:'account_number', label:__('Account Number'),
			description: __("Number of new Account, it will be included in the account name as a prefix")},
		{fieldtype:'Check', fieldname:'is_group', label:__('Is Group'),
			description: __('Further accounts can be made under Groups, but entries can be made against non-Groups')},
		{fieldtype:'Select', fieldname:'root_type', label:__('Root Type'),
			options: ['Asset', 'Liability', 'Equity', 'Income', 'Expense'].join('\n'),
			depends_on: 'eval:doc.is_group && !doc.parent_account'},
		{fieldtype:'Select', fieldname:'account_type', label:__('Account Type'),
			options: dataent.get_meta("Account").fields.filter(d => d.fieldname=='account_type')[0].options,
			description: __("Optional. This setting will be used to filter in various transactions.")
		},
		{fieldtype:'Float', fieldname:'tax_rate', label:__('Tax Rate'),
			depends_on: 'eval:doc.is_group==0&&doc.account_type=="Tax"'},
		{fieldtype:'Link', fieldname:'account_currency', label:__('Currency'), options:"Currency",
			description: __("Optional. Sets company's default currency, if not specified.")}
	],
	ignore_fields:["parent_account"],
	onload: function(treeview) {
		dataent.treeview_settings['Account'].treeview = {};
		$.extend(dataent.treeview_settings['Account'].treeview, treeview);
		function get_company() {
			return treeview.page.fields_dict.company.get_value();
		}

		// tools
		treeview.page.add_inner_button(__("Chart of Cost Centers"), function() {
			dataent.set_route('Tree', 'Cost Center', {company: get_company()});
		}, __('View'));

		treeview.page.add_inner_button(__("Opening Invoice Creation Tool"), function() {
			dataent.set_route('Form', 'Opening Invoice Creation Tool', {company: get_company()});
		}, __('View'));

		treeview.page.add_inner_button(__("Period Closing Voucher"), function() {
			dataent.set_route('List', 'Period Closing Voucher', {company: get_company()});
		}, __('View'));

		// make
		treeview.page.add_inner_button(__("Journal Entry"), function() {
			dataent.new_doc('Journal Entry', {company: get_company()});
		}, __('Make'));
		treeview.page.add_inner_button(__("New Company"), function() {
			dataent.new_doc('Company');
		}, __('Make'));

		// financial statements
		for (let report of ['Trial Balance', 'General Ledger', 'Balance Sheet',
			'Profit and Loss Statement', 'Cash Flow Statement', 'Accounts Payable', 'Accounts Receivable']) {
			treeview.page.add_inner_button(__(report), function() {
				dataent.set_route('query-report', report, {company: get_company()});
			}, __('Financial Statements'));
		}

	},
	post_render: function(treeview) {
		dataent.treeview_settings['Account'].treeview["tree"] = treeview.tree;
		treeview.page.set_primary_action(__("New"), function() {
			let root_company = treeview.page.fields_dict.root_company.get_value();

			if(root_company) {
				dataent.throw(__("Please add the account to root level Company - ") + root_company);
			} else {
				treeview.new_node();
			}
		}, "octicon octicon-plus");
	},
	onrender: function(node) {
		if(dataent.boot.user.can_read.indexOf("GL Entry") !== -1){
			var dr_or_cr = node.data.balance < 0 ? "Cr" : "Dr";
			if (node.data && node.data.balance!==undefined) {
				$('<span class="balance-area pull-right text-muted small">'
					+ (node.data.balance_in_account_currency ?
						(format_currency(Math.abs(node.data.balance_in_account_currency),
							node.data.account_currency) + " / ") : "")
					+ format_currency(Math.abs(node.data.balance), node.data.company_currency)
					+ " " + dr_or_cr
					+ '</span>').insertBefore(node.$ul);
			}
		}
	},
	toolbar: [
		{
			label:__("Add Child"),
			condition: function(node) {
				return dataent.boot.user.can_create.indexOf("Account") !== -1
					&& (!dataent.treeview_settings['Account'].treeview.page.fields_dict.root_company.get_value()
					|| dataent.flags.ignore_root_company_validation)
					&& node.expandable && !node.hide_add;
			},
			click: function() {
				var me = dataent.treeview_settings['Account'].treeview;
				me.new_node();
			},
			btnClass: "hidden-xs"
		},
		{
			condition: function(node) {
				return !node.root && dataent.boot.user.can_read.indexOf("GL Entry") !== -1
			},
			label: __("View Ledger"),
			click: function(node, btn) {
				dataent.route_options = {
					"account": node.label,
					"from_date": dataent.sys_defaults.year_start_date,
					"to_date": dataent.sys_defaults.year_end_date,
					"company": dataent.treeview_settings['Account'].treeview.page.fields_dict.company.get_value()
				};
				dataent.set_route("query-report", "General Ledger");
			},
			btnClass: "hidden-xs"
		}
	],
	extend_toolbar: true
}
