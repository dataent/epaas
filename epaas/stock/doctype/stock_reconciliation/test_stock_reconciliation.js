QUnit.module('Stock');

QUnit.test("test Stock Reconciliation", function(assert) {
	assert.expect(1);
	let done = assert.async();
	dataent.run_serially([
		() => dataent.set_route('List', 'Stock Reconciliation'),
		() => dataent.timeout(1),
		() => dataent.click_button('New'),
		() => cur_frm.set_value('company','For Testing'),
		() => dataent.click_button('Items'),
		() => {cur_dialog.set_value('warehouse','Stores - FT'); },
		() => dataent.timeout(0.5),
		() => dataent.click_button('Update'),
		() => {
			cur_frm.doc.items[0].qty = 150;
			cur_frm.refresh_fields('items');},
		() => dataent.timeout(0.5),
		() => cur_frm.set_value('expense_account','Stock Adjustment - FT'),
		() => cur_frm.set_value('cost_center','Main - FT'),
		() => cur_frm.save(),
		() => {
			// get_item_details
			assert.ok(cur_frm.doc.expense_account=='Stock Adjustment - FT', "expense_account correct");
		},
		() => dataent.tests.click_button('Submit'),
		() => dataent.tests.click_button('Yes'),
		() => dataent.timeout(0.3),
		() => done()
	]);
});

