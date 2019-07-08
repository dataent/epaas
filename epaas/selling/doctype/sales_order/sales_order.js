// Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

{% include 'epaas/selling/sales_common.js' %}

dataent.ui.form.on("Sales Order", {
	setup: function(frm) {
		frm.custom_make_buttons = {
			'Delivery Note': 'Delivery',
			'Sales Invoice': 'Invoice',
			'Material Request': 'Material Request',
			'Purchase Order': 'Purchase Order',
			'Project': 'Project'
		}
		frm.add_fetch('customer', 'tax_id', 'tax_id');

		// formatter for material request item
		frm.set_indicator_formatter('item_code',
			function(doc) { return (doc.stock_qty<=doc.delivered_qty) ? "green" : "orange" })

		frm.set_query('company_address', function(doc) {
			if(!doc.company) {
				dataent.throw(__('Please set Company'));
			}

			return {
				query: 'dataent.contacts.doctype.address.address.address_query',
				filters: {
					link_doctype: 'Company',
					link_name: doc.company
				}
			};
		})
	},
	refresh: function(frm) {
		if(frm.doc.docstatus == 1 && frm.doc.status == 'To Deliver and Bill') {
			frm.add_custom_button(__('Update Items'), () => {
				epaas.utils.update_child_items({
					frm: frm,
					child_docname: "items",
					child_doctype: "Sales Order Detail",
				})
			});
		}
	},
	onload: function(frm) {
		if (!frm.doc.transaction_date){
			frm.set_value('transaction_date', dataent.datetime.get_today())
		}
		epaas.queries.setup_queries(frm, "Warehouse", function() {
			return epaas.queries.warehouse(frm.doc);
		});

		frm.set_query('project', function(doc, cdt, cdn) {
			return {
				query: "epaas.controllers.queries.get_project_name",
				filters: {
					'customer': doc.customer
				}
			}
		});

		frm.set_query("blanket_order", "items", function() {
			return {
				filters: {
					"company": frm.doc.company,
					"docstatus": 1
				}
			}
		});

		epaas.queries.setup_warehouse_query(frm);
	},

	delivery_date: function(frm) {
		$.each(frm.doc.items || [], function(i, d) {
			if(!d.delivery_date) d.delivery_date = frm.doc.delivery_date;
		});
		refresh_field("items");
	}
});

dataent.ui.form.on("Sales Order Item", {
	item_code: function(frm,cdt,cdn) {
		var row = locals[cdt][cdn];
		if (frm.doc.delivery_date) {
			row.delivery_date = frm.doc.delivery_date;
			refresh_field("delivery_date", cdn, "items");
		} else {
			frm.script_manager.copy_from_first_row("items", row, ["delivery_date"]);
		}
	},
	delivery_date: function(frm, cdt, cdn) {
		if(!frm.doc.delivery_date) {
			epaas.utils.copy_value_in_all_rows(frm.doc, cdt, cdn, "items", "delivery_date");
		}
	}
});

epaas.selling.SalesOrderController = epaas.selling.SellingController.extend({
	onload: function(doc, dt, dn) {
		this._super();
	},

	refresh: function(doc, dt, dn) {
		var me = this;
		this._super();
		var allow_purchase = false;
		var allow_delivery = false;

		if(doc.docstatus==1) {
			if(doc.status != 'Closed') {

				for (var i in this.frm.doc.items) {
					var item = this.frm.doc.items[i];
					if(item.delivered_by_supplier === 1 || item.supplier){
						if(item.qty > flt(item.ordered_qty)
							&& item.qty > flt(item.delivered_qty)) {
							allow_purchase = true;
						}
					}

					if (item.delivered_by_supplier===0) {
						if(item.qty > flt(item.delivered_qty)) {
							allow_delivery = true;
						}
					}

					if (allow_delivery && allow_purchase) {
						break;
					}
				}

				if (this.frm.has_perm("submit")) {
					// close
					if(flt(doc.per_delivered, 6) < 100 || flt(doc.per_billed, 6) < 100) {
						this.frm.add_custom_button(__('Close'),
							function() { me.close_sales_order() }, __("Status"))
					}
				}

				// delivery note
				if(flt(doc.per_delivered, 6) < 100 && allow_delivery) {
					this.frm.add_custom_button(__('Delivery'),
						function() { me.make_delivery_note_based_on_delivery_date(); }, __("Make"));

					if(["Sales", "Shopping Cart"].indexOf(doc.order_type)!==-1){
						this.frm.add_custom_button(__('Work Order'),
							function() { me.make_work_order() }, __("Make"));

						}
					this.frm.page.set_inner_btn_group_as_primary(__("Make"));
				}

				// sales invoice
				if(flt(doc.per_billed, 6) < 100) {
					this.frm.add_custom_button(__('Invoice'),
						function() { me.make_sales_invoice() }, __("Make"));
				}

				// material request
				if(!doc.order_type || ["Sales", "Shopping Cart"].indexOf(doc.order_type)!==-1
					&& flt(doc.per_delivered, 6) < 100) {
					this.frm.add_custom_button(__('Material Request'),
						function() { me.make_material_request() }, __("Make"));
					this.frm.add_custom_button(__('Request for Raw Materials'),
						function() { me.make_raw_material_request() }, __("Make"));
				}

				// make purchase order
				if(flt(doc.per_delivered, 6) < 100 && allow_purchase) {
					this.frm.add_custom_button(__('Purchase Order'),
						function() { me.make_purchase_order() }, __("Make"));
				}

				// payment request
				if(flt(doc.per_billed)==0) {
					this.frm.add_custom_button(__('Payment Request'),
						function() { me.make_payment_request() }, __("Make"));
					this.frm.add_custom_button(__('Payment'),
						function() { me.make_payment_entry() }, __("Make"));
				}

				// maintenance
				if(flt(doc.per_delivered, 2) < 100 &&
						["Sales", "Shopping Cart"].indexOf(doc.order_type)===-1) {
					this.frm.add_custom_button(__('Maintenance Visit'),
						function() { me.make_maintenance_visit() }, __("Make"));
					this.frm.add_custom_button(__('Maintenance Schedule'),
						function() { me.make_maintenance_schedule() }, __("Make"));
				}

				// project
				if(flt(doc.per_delivered, 2) < 100 && ["Sales", "Shopping Cart"].indexOf(doc.order_type)!==-1 && allow_delivery) {
						this.frm.add_custom_button(__('Project'),
							function() { me.make_project() }, __("Make"));
				}

				if(!doc.auto_repeat) {
					this.frm.add_custom_button(__('Subscription'), function() {
						epaas.utils.make_subscription(doc.doctype, doc.name)
					}, __("Make"))
				}

			} else {
				if (this.frm.has_perm("submit")) {
					// un-close
					this.frm.add_custom_button(__('Re-open'), function() {
						me.frm.cscript.update_status('Re-open', 'Draft')
					}, __("Status"));
				}
			}
		}

		if (this.frm.doc.docstatus===0) {
			this.frm.add_custom_button(__('Quotation'),
				function() {
					epaas.utils.map_current_doc({
						method: "epaas.selling.doctype.quotation.quotation.make_sales_order",
						source_doctype: "Quotation",
						target: me.frm,
						setters: [
							{
								label: "Customer",
								fieldname: "party_name",
								fieldtype: "Link",
								options: "Customer",
								default: me.frm.doc.customer || undefined
							}
						],
						get_query_filters: {
							company: me.frm.doc.company,
							docstatus: 1,
							status: ["!=", "Lost"]
						}
					})
				}, __("Get items from"));
		}

		this.order_type(doc);
	},

	make_work_order() {
		var me = this;
		this.frm.call({
			doc: this.frm.doc,
			method: 'get_work_order_items',
			callback: function(r) {
				if(!r.message) {
					dataent.msgprint({
						title: __('Work Order not created'),
						message: __('No Items with Bill of Materials to Manufacture'),
						indicator: 'orange'
					});
					return;
				}
				else if(!r.message) {
					dataent.msgprint({
						title: __('Work Order not created'),
						message: __('Work Order already created for all items with BOM'),
						indicator: 'orange'
					});
					return;
				} else {
					var fields = [
						{fieldtype:'Table', fieldname: 'items',
							description: __('Select BOM and Qty for Production'),
							fields: [
								{fieldtype:'Read Only', fieldname:'item_code',
									label: __('Item Code'), in_list_view:1},
								{fieldtype:'Link', fieldname:'bom', options: 'BOM', reqd: 1,
									label: __('Select BOM'), in_list_view:1, get_query: function(doc) {
										return {filters: {item: doc.item_code}};
									}},
								{fieldtype:'Float', fieldname:'pending_qty', reqd: 1,
									label: __('Qty'), in_list_view:1},
								{fieldtype:'Data', fieldname:'sales_order_item', reqd: 1,
									label: __('Sales Order Item'), hidden:1}
							],
							data: r.message,
							get_data: function() {
								return r.message
							}
						}
					]
					var d = new dataent.ui.Dialog({
						title: __('Select Items to Manufacture'),
						fields: fields,
						primary_action: function() {
							var data = d.get_values();
							me.frm.call({
								method: 'make_work_orders',
								args: {
									items: data,
									company: me.frm.doc.company,
									sales_order: me.frm.docname,
									project: me.frm.project
								},
								freeze: true,
								callback: function(r) {
									if(r.message) {
										dataent.msgprint({
											message: __('Work Orders Created: {0}',
												[r.message.map(function(d) {
													return repl('<a href="#Form/Work Order/%(name)s">%(name)s</a>', {name:d})
												}).join(', ')]),
											indicator: 'green'
										})
									}
									d.hide();
								}
							});
						},
						primary_action_label: __('Make')
					});
					d.show();
				}
			}
		});
	},

	order_type: function() {
		this.frm.fields_dict.items.grid.toggle_reqd("delivery_date", this.frm.doc.order_type == "Sales");
	},

	tc_name: function() {
		this.get_terms();
	},

	make_material_request: function() {
		dataent.model.open_mapped_doc({
			method: "epaas.selling.doctype.sales_order.sales_order.make_material_request",
			frm: this.frm
		})
	},

	make_raw_material_request: function() {
		var me = this;
		this.frm.call({
			doc: this.frm.doc,
			method: 'get_work_order_items',
			args: {
				for_raw_material_request: 1
			},
			callback: function(r) {
				if(!r.message) {
					dataent.msgprint({
						message: __('No Items with Bill of Materials.'),
						indicator: 'orange'
					});
					return;
				}
				else {
					me.make_raw_material_request_dialog(r);
				}
			}
		});
	},

	make_raw_material_request_dialog: function(r) {
		var fields = [
			{fieldtype:'Check', fieldname:'include_exploded_items',
				label: __('Include Exploded Items')},
			{fieldtype:'Check', fieldname:'ignore_existing_ordered_qty',
				label: __('Ignore Existing Ordered Qty')},
			{
				fieldtype:'Table', fieldname: 'items',
				description: __('Select BOM, Qty and For Warehouse'),
				fields: [
					{fieldtype:'Read Only', fieldname:'item_code',
						label: __('Item Code'), in_list_view:1},
					{fieldtype:'Link', fieldname:'bom', options: 'BOM', reqd: 1,
						label: __('BOM'), in_list_view:1, get_query: function(doc) {
							return {filters: {item: doc.item_code}};
						}
					},
					{fieldtype:'Float', fieldname:'required_qty', reqd: 1,
						label: __('Qty'), in_list_view:1},
					{fieldtype:'Link', fieldname:'for_warehouse', options: 'Warehouse',
						label: __('For Warehouse')}
				],
				data: r.message,
				get_data: function() {
					return r.message
				}
			}
		]
		var d = new dataent.ui.Dialog({
			title: __("Items for Raw Material Request"),
			fields: fields,
			primary_action: function() {
				var data = d.get_values();
				me.frm.call({
					method: 'epaas.selling.doctype.sales_order.sales_order.make_raw_material_request',
					args: {
						items: data,
						company: me.frm.doc.company,
						sales_order: me.frm.docname,
						project: me.frm.project
					},
					freeze: true,
					callback: function(r) {
						if(r.message) {
							dataent.msgprint(__('Material Request {0} submitted.',
							['<a href="#Form/Material Request/'+r.message.name+'">' + r.message.name+ '</a>']));
						}
						d.hide();
						me.frm.reload_doc();
					}
				});
			},
			primary_action_label: __('Make')
		});
		d.show();
	},

	make_delivery_note_based_on_delivery_date: function() {
		var me = this;

		var delivery_dates = [];
		$.each(this.frm.doc.items || [], function(i, d) {
			if(!delivery_dates.includes(d.delivery_date)) {
				delivery_dates.push(d.delivery_date);
			}
		});

		var item_grid = this.frm.fields_dict["items"].grid;
		if(!item_grid.get_selected().length && delivery_dates.length > 1) {
			var dialog = new dataent.ui.Dialog({
				title: __("Select Items based on Delivery Date"),
				fields: [{fieldtype: "HTML", fieldname: "dates_html"}]
			});

			var html = $(`
				<div style="border: 1px solid #d1d8dd">
					<div class="list-item list-item--head">
						<div class="list-item__content list-item__content--flex-2">
							${__('Delivery Date')}
						</div>
					</div>
					${delivery_dates.map(date => `
						<div class="list-item">
							<div class="list-item__content list-item__content--flex-2">
								<label>
								<input type="checkbox" data-date="${date}" checked="checked"/>
								${dataent.datetime.str_to_user(date)}
								</label>
							</div>
						</div>
					`).join("")}
				</div>
			`);

			var wrapper = dialog.fields_dict.dates_html.$wrapper;
			wrapper.html(html);

			dialog.set_primary_action(__("Select"), function() {
				var dates = wrapper.find('input[type=checkbox]:checked')
					.map((i, el) => $(el).attr('data-date')).toArray();

				if(!dates) return;

				$.each(dates, function(i, d) {
					$.each(item_grid.grid_rows || [], function(j, row) {
						if(row.doc.delivery_date == d) {
							row.doc.__checked = 1;
						}
					});
				})
				me.make_delivery_note();
				dialog.hide();
			});
			dialog.show();
		} else {
			this.make_delivery_note();
		}
	},

	make_delivery_note: function() {
		dataent.model.open_mapped_doc({
			method: "epaas.selling.doctype.sales_order.sales_order.make_delivery_note",
			frm: me.frm
		})
	},

	make_sales_invoice: function() {
		dataent.model.open_mapped_doc({
			method: "epaas.selling.doctype.sales_order.sales_order.make_sales_invoice",
			frm: this.frm
		})
	},

	make_maintenance_schedule: function() {
		dataent.model.open_mapped_doc({
			method: "epaas.selling.doctype.sales_order.sales_order.make_maintenance_schedule",
			frm: this.frm
		})
	},

	make_project: function() {
		dataent.model.open_mapped_doc({
			method: "epaas.selling.doctype.sales_order.sales_order.make_project",
			frm: this.frm
		})
	},

	make_maintenance_visit: function() {
		dataent.model.open_mapped_doc({
			method: "epaas.selling.doctype.sales_order.sales_order.make_maintenance_visit",
			frm: this.frm
		})
	},

	make_purchase_order: function(){
		var me = this;
		var dialog = new dataent.ui.Dialog({
			title: __("For Supplier"),
			fields: [
				{"fieldtype": "Link", "label": __("Supplier"), "fieldname": "supplier", "options":"Supplier",
				 "description": __("Leave the field empty to make purchase orders for all suppliers"),
					"get_query": function () {
						return {
							query:"epaas.selling.doctype.sales_order.sales_order.get_supplier",
							filters: {'parent': me.frm.doc.name}
						}
					}},

				{"fieldtype": "Button", "label": __("Make Purchase Order"), "fieldname": "make_purchase_order", "cssClass": "btn-primary"},
			]
		});

		dialog.fields_dict.make_purchase_order.$input.click(function() {
			var args = dialog.get_values();
			dialog.hide();
			return dataent.call({
				type: "GET",
				method: "epaas.selling.doctype.sales_order.sales_order.make_purchase_order_for_drop_shipment",
				args: {
					"source_name": me.frm.doc.name,
					"for_supplier": args.supplier
				},
				freeze: true,
				callback: function(r) {
					if(!r.exc) {
						// var args = dialog.get_values();
						if (args.supplier){
							var doc = dataent.model.sync(r.message);
							dataent.set_route("Form", r.message.doctype, r.message.name);
						}
						else{
							dataent.route_options = {
								"sales_order": me.frm.doc.name
							}
							dataent.set_route("List", "Purchase Order");
						}
					}
				}
			})
		});
		dialog.show();
	},
	close_sales_order: function(){
		this.frm.cscript.update_status("Close", "Closed")
	},
	update_status: function(label, status){
		var doc = this.frm.doc;
		var me = this;
		dataent.ui.form.is_saving = true;
		dataent.call({
			method: "epaas.selling.doctype.sales_order.sales_order.update_status",
			args: {status: status, name: doc.name},
			callback: function(r){
				me.frm.reload_doc();
			},
			always: function() {
				dataent.ui.form.is_saving = false;
			}
		});
	}
});
$.extend(cur_frm.cscript, new epaas.selling.SalesOrderController({frm: cur_frm}));
