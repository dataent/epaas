QUnit.module('Stock');

QUnit.test("test delivery note with margin", function(assert) {
	assert.expect(3);
	let done = assert.async();
	dataent.run_serially([
		() => {
			return dataent.tests.make('Delivery Note', [
				{customer:'Test Customer 1'},
				{selling_price_list: 'Test-Selling-USD'},
				{currency: 'USD'},
				{items: [
					[
						{'item_code': 'Test Product 4'},
						{'qty': 1},
						{'margin_type': 'Amount'},
						{'margin_rate_or_amount': 10}
					]
				]},
			]);
		},

		() => cur_frm.save(),
		() => {
			// get_rate_details
			assert.ok(cur_frm.doc.items[0].rate_with_margin == 210, "Margin rate correct");
			assert.ok(cur_frm.doc.items[0].base_rate_with_margin == cur_frm.doc.conversion_rate * 210, "Base margin rate correct");
			assert.ok(cur_frm.doc.total == 210, "Amount correct");
		},

		() => dataent.tests.click_button('Submit'),
		() => dataent.tests.click_button('Yes'),
		() => dataent.timeout(0.3),
		() => done()
	]);
});

