QUnit.module('buying');

QUnit.test("Test: Request for Quotation", function (assert) {
	assert.expect(5);
	let done = assert.async();
	let rfq_name = "";

	dataent.run_serially([
		// Go to RFQ list
		() => dataent.set_route("List", "Request for Quotation"),
		// Create a new RFQ
		() => dataent.new_doc("Request for Quotation"),
		() => dataent.timeout(1),
		() => cur_frm.set_value("transaction_date", "04-04-2017"),
		() => cur_frm.set_value("company", "For Testing"),
		// Add Suppliers
		() => {
			cur_frm.fields_dict.suppliers.grid.grid_rows[0].toggle_view();
		},
		() => dataent.timeout(1),
		() => {
			cur_frm.fields_dict.suppliers.grid.grid_rows[0].doc.supplier = "_Test Supplier";
			dataent.click_check('Send Email');
			cur_frm.cur_grid.frm.script_manager.trigger('supplier');
		},
		() => dataent.timeout(1),
		() => {
			cur_frm.cur_grid.toggle_view();
		},
		() => dataent.timeout(1),
		() => dataent.click_button('Add Row',0),
		() => dataent.timeout(1),
		() => {
			cur_frm.fields_dict.suppliers.grid.grid_rows[1].toggle_view();
		},
		() => dataent.timeout(1),
		() => {
			cur_frm.fields_dict.suppliers.grid.grid_rows[1].doc.supplier = "_Test Supplier 1";
			dataent.click_check('Send Email');
			cur_frm.cur_grid.frm.script_manager.trigger('supplier');
		},
		() => dataent.timeout(1),
		() => {
			cur_frm.cur_grid.toggle_view();
		},
		() => dataent.timeout(1),
		// Add Item
		() => {
			cur_frm.fields_dict.items.grid.grid_rows[0].toggle_view();
		},
		() => dataent.timeout(1),
		() => {
			cur_frm.fields_dict.items.grid.grid_rows[0].doc.item_code = "_Test Item";
			dataent.set_control('item_code',"_Test Item");
			dataent.set_control('qty',5);
			dataent.set_control('schedule_date', "05-05-2017");
			cur_frm.cur_grid.frm.script_manager.trigger('supplier');
		},
		() => dataent.timeout(2),
		() => {
			cur_frm.cur_grid.toggle_view();
		},
		() => dataent.timeout(2),
		() => {
			cur_frm.fields_dict.items.grid.grid_rows[0].doc.warehouse = "_Test Warehouse - FT";
		},
		() => dataent.click_button('Save'),
		() => dataent.timeout(1),
		() => dataent.click_button('Submit'),
		() => dataent.timeout(1),
		() => dataent.click_button('Yes'),
		() => dataent.timeout(1),
		() => dataent.click_button('Menu'),
		() => dataent.timeout(1),
		() => dataent.click_link('Reload'),
		() => dataent.timeout(1),
		() => {
			assert.equal(cur_frm.doc.docstatus, 1);
			rfq_name = cur_frm.doc.name;
			assert.ok(cur_frm.fields_dict.suppliers.grid.grid_rows[0].doc.quote_status == "Pending");
			assert.ok(cur_frm.fields_dict.suppliers.grid.grid_rows[1].doc.quote_status == "Pending");
		},
		() => {
			cur_frm.fields_dict.suppliers.grid.grid_rows[0].toggle_view();
		},
		() => dataent.timeout(1),
		() => {
			dataent.click_check('No Quote');
		},
		() => dataent.timeout(1),
		() => {
			cur_frm.cur_grid.toggle_view();
		},
		() => dataent.click_button('Update'),
		() => dataent.timeout(1),

		() => dataent.click_button('Supplier Quotation'),
		() => dataent.timeout(1),
		() => dataent.click_link('Make'),
		() => dataent.timeout(1),
		() => {
			dataent.set_control('supplier',"_Test Supplier 1");
		},
		() => dataent.timeout(1),
		() => dataent.click_button('Make Supplier Quotation'),
		() => dataent.timeout(1),
		() => cur_frm.set_value("company", "For Testing"),
		() => cur_frm.fields_dict.items.grid.grid_rows[0].doc.rate = 4.99,
		() => dataent.timeout(1),
		() => dataent.click_button('Save'),
		() => dataent.timeout(1),
		() => dataent.click_button('Submit'),
		() => dataent.timeout(1),
		() => dataent.click_button('Yes'),
		() => dataent.timeout(1),
		() => dataent.set_route("List", "Request for Quotation"),
		() => dataent.timeout(2),
		() => dataent.set_route("List", "Request for Quotation"),
		() => dataent.timeout(2),
		() => dataent.click_link(rfq_name),
		() => dataent.timeout(1),
		() => dataent.click_button('Menu'),
		() => dataent.timeout(1),
		() => dataent.click_link('Reload'),
		() => dataent.timeout(1),
		() => {
			assert.ok(cur_frm.fields_dict.suppliers.grid.grid_rows[1].doc.quote_status == "Received");
			assert.ok(cur_frm.fields_dict.suppliers.grid.grid_rows[0].doc.no_quote == 1);
		},
		() => done()
	]);
});