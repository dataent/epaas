// Copyright (c) 2017, Dataent Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

dataent.ui.form.on('Delivery Trip', {
	setup: function (frm) {
		frm.set_indicator_formatter('customer', (stop) => (stop.visited) ? "green" : "orange");

		frm.set_query("driver", function () {
			return {
				filters: {
					"status": "Active"
				}
			};
		});

		frm.set_query("address", "delivery_stops", function (doc, cdt, cdn) {
			var row = locals[cdt][cdn];
			if (row.customer) {
				return {
					query: 'dataent.contacts.doctype.address.address.address_query',
					filters: {
						link_doctype: "Customer",
						link_name: row.customer
					}
				};
			}
		})

		frm.set_query("contact", "delivery_stops", function (doc, cdt, cdn) {
			var row = locals[cdt][cdn];
			if (row.customer) {
				return {
					query: 'dataent.contacts.doctype.contact.contact.contact_query',
					filters: {
						link_doctype: "Customer",
						link_name: row.customer
					}
				};
			}
		})
	},

	refresh: function (frm) {
		if (frm.doc.docstatus == 1 && frm.doc.delivery_stops.length > 0) {
			frm.add_custom_button(__("Notify Customers via Email"), function () {
				frm.trigger('notify_customers');
			});
		}

		if (frm.doc.docstatus === 0) {
			frm.add_custom_button(__('Delivery Note'), () => {
				epaas.utils.map_current_doc({
					method: "epaas.stock.doctype.delivery_note.delivery_note.make_delivery_trip",
					source_doctype: "Delivery Note",
					target: frm,
					date_field: "posting_date",
					setters: {
						company: frm.doc.company,
					},
					get_query_filters: {
						docstatus: 1,
						company: frm.doc.company,
					}
				})
			}, __("Get customers from"));
		}
	},

	calculate_arrival_time: function (frm) {
		dataent.db.get_value("Google Maps Settings", { name: "Google Maps Settings" }, "enabled", (r) => {
			if (r.enabled == 0) {
				dataent.throw(__("Please enable Google Maps Settings to estimate and optimize routes"));
			} else {
				dataent.call({
					method: 'epaas.stock.doctype.delivery_trip.delivery_trip.get_arrival_times',
					freeze: true,
					freeze_message: __("Updating estimated arrival times."),
					args: {
						delivery_trip: frm.doc.name,
					},
					callback: function (r) {
						frm.reload_doc();
					}
				});
			}
		})
	},

	optimize_route: function (frm) {
		dataent.db.get_value("Google Maps Settings", {name: "Google Maps Settings"}, "enabled", (r) => {
			if (r.enabled == 0) {
				dataent.throw(__("Please enable Google Maps Settings to estimate and optimize routes"));
			} else {
				dataent.call({
					method: 'epaas.stock.doctype.delivery_trip.delivery_trip.optimize_route',
					freeze: true,
					freeze_message: __("Optimizing routes."),
					args: {
						delivery_trip: frm.doc.name,
					},
					callback: function (r) {
						frm.reload_doc();
					}
				});
			}
		})
	},

	notify_customers: function (frm) {
		$.each(frm.doc.delivery_stops || [], function (i, delivery_stop) {
			if (!delivery_stop.delivery_note) {
				dataent.msgprint({
					"message": __("No Delivery Note selected for Customer {}", [delivery_stop.customer]),
					"title": __("Warning"),
					"indicator": "orange",
					"alert": 1
				});
			}
		});

		dataent.db.get_value("Delivery Settings", { name: "Delivery Settings" }, "dispatch_template", (r) => {
			if (!r.dispatch_template) {
				dataent.throw(__("Missing email template for dispatch. Please set one in Delivery Settings."));
			} else {
				dataent.confirm(__("Do you want to notify all the customers by email?"), function () {
					dataent.call({
						method: "epaas.stock.doctype.delivery_trip.delivery_trip.notify_customers",
						args: {
							"delivery_trip": frm.doc.name
						},
						callback: function (r) {
							if (!r.exc) {
								frm.doc.email_notification_sent = true;
								frm.refresh_field('email_notification_sent');
							}
						}
					});
				});
			}
		});
	}
});

dataent.ui.form.on('Delivery Stop', {
	customer: function (frm, cdt, cdn) {
		var row = locals[cdt][cdn];
		if (row.customer) {
			dataent.call({
				method: "epaas.stock.doctype.delivery_trip.delivery_trip.get_contact_and_address",
				args: { "name": row.customer },
				callback: function (r) {
					if (r.message) {
						if (r.message["shipping_address"]) {
							dataent.model.set_value(cdt, cdn, "address", r.message["shipping_address"].parent);
						}
						else {
							dataent.model.set_value(cdt, cdn, "address", '');
						}
						if (r.message["contact_person"]) {
							dataent.model.set_value(cdt, cdn, "contact", r.message["contact_person"].parent);
						}
						else {
							dataent.model.set_value(cdt, cdn, "contact", '');
						}
					}
					else {
						dataent.model.set_value(cdt, cdn, "address", '');
						dataent.model.set_value(cdt, cdn, "contact", '');
					}
				}
			});
		}
	},

	address: function (frm, cdt, cdn) {
		var row = locals[cdt][cdn];
		if (row.address) {
			dataent.call({
				method: "dataent.contacts.doctype.address.address.get_address_display",
				args: { "address_dict": row.address },
				callback: function (r) {
					if (r.message) {
						dataent.model.set_value(cdt, cdn, "customer_address", r.message);
					}
				}
			});
		} else {
			dataent.model.set_value(cdt, cdn, "customer_address", "");
		}
	},

	contact: function (frm, cdt, cdn) {
		var row = locals[cdt][cdn];
		if (row.contact) {
			dataent.call({
				method: "epaas.stock.doctype.delivery_trip.delivery_trip.get_contact_display",
				args: { "contact": row.contact },
				callback: function (r) {
					if (r.message) {
						dataent.model.set_value(cdt, cdn, "customer_contact", r.message);
					}
				}
			});
		} else {
			dataent.model.set_value(cdt, cdn, "customer_contact", "");
		}
	}
});