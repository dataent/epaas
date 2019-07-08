QUnit.module('Quotation');

QUnit.test("test quotation with multi uom", function(assert) {
	assert.expect(3);
	let done = assert.async();
	dataent.run_serially([
		() => {
			return dataent.tests.make('Quotation', [
				{customer: 'Test Customer 1'},
				{items: [
					[
						{'delivery_date': dataent.datetime.add_days(dataent.defaults.get_default("year_end_date"), 1)},
						{'qty': 5},
						{'item_code': 'Test Product 4'},
						{'uom': 'unit'},
					]
				]},
				{customer_address: 'Test1-Billing'},
				{shipping_address_name: 'Test1-Shipping'},
				{contact_person: 'Contact 1-Test Customer 1'}
			]);
		},
		() => cur_frm.save(),
		() => {
			// get_item_details
			assert.ok(cur_frm.doc.items[0].item_name=='Test Product 4', "Item name correct");
			// get uom details
			assert.ok(cur_frm.doc.items[0].uom=='Unit', "Multi Uom correct");
			// get grand_total details
			assert.ok(cur_frm.doc.grand_total== 5000, "Grand total correct ");

		},
		() => dataent.tests.click_button('Submit'),
		() => dataent.tests.click_button('Yes'),
		() => dataent.timeout(0.3),
		() => done()
	]);
});

