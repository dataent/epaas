QUnit.test("test: opportunity", function (assert) {
	assert.expect(8);
	let done = assert.async();
	dataent.run_serially([
		() => dataent.set_route('List', 'Opportunity'),
		() => dataent.timeout(1),
		() => dataent.click_button('New'),
		() => dataent.timeout(1),
		() => cur_frm.set_value('opportunity_from', 'Customer'),
		() => cur_frm.set_value('customer', 'Test Customer 1'),

		// check items
		() => cur_frm.set_value('with_items', 1),
		() => dataent.tests.set_grid_values(cur_frm, 'items', [
			[
				{item_code:'Test Product 1'},
				{qty: 4}
			]
		]),
		() => cur_frm.save(),
		() => dataent.timeout(1),
		() => {
			assert.notOk(cur_frm.is_new(), 'saved');
			dataent.opportunity_name = cur_frm.doc.name;
		},

		// close and re-open
		() => dataent.click_button('Close'),
		() => dataent.timeout(1),
		() => assert.equal(cur_frm.doc.status, 'Closed',
			'closed'),

		() => dataent.click_button('Reopen'),
		() => assert.equal(cur_frm.doc.status, 'Open',
			'reopened'),
		() => dataent.timeout(1),

		// make quotation
		() => dataent.click_button('Make'),
		() => dataent.click_link('Quotation', 1),
		() => dataent.timeout(2),
		() => {
			assert.equal(dataent.get_route()[1], 'Quotation',
				'made quotation');
			assert.equal(cur_frm.doc.customer, 'Test Customer 1',
				'customer set in quotation');
			assert.equal(cur_frm.doc.items[0].item_code, 'Test Product 1',
				'item set in quotation');
			assert.equal(cur_frm.doc.items[0].qty, 4,
				'qty set in quotation');
			assert.equal(cur_frm.doc.items[0].prevdoc_docname, dataent.opportunity_name,
				'opportunity set in quotation');
		},
		() => done()
	]);
});
