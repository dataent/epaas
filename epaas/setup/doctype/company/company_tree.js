dataent.treeview_settings["Company"] = {
	ignore_fields:["parent_company"],
	get_tree_nodes: 'epaas.setup.doctype.company.company.get_children',
	add_tree_node: 'epaas.setup.doctype.company.company.add_node',
	filters: [
		{
			fieldname: "company",
			fieldtype:"Link",
			options: "Company",
			label: __("Company"),
			get_query: function() {
				return {
					filters: [["Company", 'is_group', '=', 1]]
				};
			}
		},
	],
	breadcrumb: "Setup",
	root_label: "All Companies",
	get_tree_root: false,
	menu_items: [
		{
			label: __("New Company"),
			action: function() {
				dataent.new_doc("Company", true);
			},
			condition: 'dataent.boot.user.can_create.indexOf("Company") !== -1'
		}
	],
	onload: function(treeview) {
		treeview.make_tree();
	}
};