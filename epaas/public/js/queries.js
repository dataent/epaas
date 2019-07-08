// Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

// searches for enabled users
dataent.provide("epaas.queries");
$.extend(epaas.queries, {
	user: function() {
		return { query: "dataent.core.doctype.user.user.user_query" };
	},

	lead: function() {
		return { query: "epaas.controllers.queries.lead_query" };
	},

	customer: function() {
		return { query: "epaas.controllers.queries.customer_query" };
	},

	supplier: function() {
		return { query: "epaas.controllers.queries.supplier_query" };
	},

	item: function(filters) {
		var args = { query: "epaas.controllers.queries.item_query" };
		if(filters) args["filters"] = filters;
		return args;
	},

	bom: function() {
		return { query: "epaas.controllers.queries.bom" };
	},

	task: function() {
		return { query: "epaas.projects.utils.query_task" };
	},

	customer_filter: function(doc) {
		if(!doc.customer) {
			dataent.throw(__("Please set {0}", [__(dataent.meta.get_label(doc.doctype, "customer", doc.name))]));
		}

		return { filters: { customer: doc.customer } };
	},

	contact_query: function(doc) {
		if(dataent.dynamic_link) {
			if(!doc[dataent.dynamic_link.fieldname]) {
				dataent.throw(__("Please set {0}",
					[__(dataent.meta.get_label(doc.doctype, dataent.dynamic_link.fieldname, doc.name))]));
			}

			return {
				query: 'dataent.contacts.doctype.contact.contact.contact_query',
				filters: {
					link_doctype: dataent.dynamic_link.doctype,
					link_name: doc[dataent.dynamic_link.fieldname]
				}
			};
		}
	},

	address_query: function(doc) {
		if(dataent.dynamic_link) {
			if(!doc[dataent.dynamic_link.fieldname]) {
				dataent.throw(__("Please set {0}",
					[__(dataent.meta.get_label(doc.doctype, dataent.dynamic_link.fieldname, doc.name))]));
			}

			return {
				query: 'dataent.contacts.doctype.address.address.address_query',
				filters: {
					link_doctype: dataent.dynamic_link.doctype,
					link_name: doc[dataent.dynamic_link.fieldname]
				}
			};
		}
	},

	company_address_query: function(doc) {
		return {
			query: 'dataent.contacts.doctype.address.address.address_query',
			filters: { is_your_company_address: 1, link_doctype: 'Company', link_name: doc.company || '' }
		};
	},

	supplier_filter: function(doc) {
		if(!doc.supplier) {
			dataent.throw(__("Please set {0}", [__(dataent.meta.get_label(doc.doctype, "supplier", doc.name))]));
		}

		return { filters: { supplier: doc.supplier } };
	},

	lead_filter: function(doc) {
		if(!doc.lead) {
			dataent.throw(__("Please specify a {0}",
				[__(dataent.meta.get_label(doc.doctype, "lead", doc.name))]));
		}

		return { filters: { lead: doc.lead } };
	},

	not_a_group_filter: function() {
		return { filters: { is_group: 0 } };
	},

	employee: function() {
		return { query: "epaas.controllers.queries.employee_query" }
	},

	warehouse: function(doc) {
		return {
			filters: [
				["Warehouse", "company", "in", ["", cstr(doc.company)]],
				["Warehouse", "is_group", "=",0]

			]
		}
	}
});

epaas.queries.setup_queries = function(frm, options, query_fn) {
	var me = this;
	var set_query = function(doctype, parentfield) {
		var link_fields = dataent.meta.get_docfields(doctype, frm.doc.name,
			{"fieldtype": "Link", "options": options});
		$.each(link_fields, function(i, df) {
			if(parentfield) {
				frm.set_query(df.fieldname, parentfield, query_fn);
			} else {
				frm.set_query(df.fieldname, query_fn);
			}
		});
	};

	set_query(frm.doc.doctype);

	// warehouse field in tables
	$.each(dataent.meta.get_docfields(frm.doc.doctype, frm.doc.name, {"fieldtype": "Table"}),
		function(i, df) {
			set_query(df.options, df.fieldname);
		});
}

/* 	if item code is selected in child table
	then list down warehouses with its quantity
	else apply default filters.
*/
epaas.queries.setup_warehouse_query = function(frm){
	frm.set_query('warehouse', 'items', function(doc, cdt, cdn) {
		var row  = locals[cdt][cdn];
		var filters = epaas.queries.warehouse(frm.doc);
		if(row.item_code){
			$.extend(filters, {"query":"epaas.controllers.queries.warehouse_query"});
			filters["filters"].push(["Bin", "item_code", "=", row.item_code]);
		}
		return filters
	});
}
