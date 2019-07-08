QUnit.module('Buying');

QUnit.test("test: purchase order receipt", function(assert) {
	assert.expect(5);
	let done = assert.async();

	dataent.run_serially([
		() => {
			return dataent.tests.make('Purchase Order', [
				{supplier: 'Test Supplier'},
				{is_subcontracted: 'No'},
				{buying_price_list: 'Test-Buying-USD'},
				{currency: 'USD'},
				{items: [
					[
						{"item_code": 'Test Product 1'},
						{"schedule_date": dataent.datetime.add_days(dataent.datetime.now_date(), 1)},
						{"expected_delivery_date": dataent.datetime.add_days(dataent.datetime.now_date(), 5)},
						{"qty": 5},
						{"uom": 'Unit'},
						{"rate": 100},
						{"warehouse": 'Stores - '+dataent.get_abbr(dataent.defaults.get_default("Company"))}
					]
				]},
			]);
		},

		() => {

			// Check supplier and item details
			assert.ok(cur_frm.doc.supplier_name == 'Test Supplier', "Supplier name correct");
			assert.ok(cur_frm.doc.items[0].item_name == 'Test Product 1', "Item name correct");
			assert.ok(cur_frm.doc.items[0].description == 'Test Product 1', "Description correct");
			assert.ok(cur_frm.doc.items[0].qty == 5, "Quantity correct");

		},

		() => dataent.timeout(1),

		() => dataent.tests.click_button('Submit'),
		() => dataent.tests.click_button('Yes'),

		() => dataent.timeout(1.5),
		() => dataent.click_button('Close'),
		() => dataent.timeout(0.3),

		// Make Purchase Receipt
		() => dataent.click_button('Make'),
		() => dataent.timeout(0.3),

		() => dataent.click_link('Receipt'),
		() => dataent.timeout(2),

		() => cur_frm.save(),

		// Save and submit Purchase Receipt
		() => dataent.timeout(1),
		() => dataent.tests.click_button('Submit'),
		() => dataent.tests.click_button('Yes'),
		() => dataent.timeout(1),

		// View Purchase order in Stock Ledger
		() => dataent.click_button('View'),
		() => dataent.timeout(0.3),

		() => dataent.click_link('Stock Ledger'),
		() => dataent.timeout(2),
		() => {
			assert.ok($('div.slick-cell.l2.r2 > a').text().includes('Test Product 1')
				&& $('div.slick-cell.l9.r9 > div').text().includes(5), "Stock ledger entry correct");
		},
		() => done()
	]);
});
