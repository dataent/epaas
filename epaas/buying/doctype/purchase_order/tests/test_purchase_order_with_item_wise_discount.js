QUnit.module('Buying');

QUnit.test("test: purchase order with item wise discount", function(assert) {
	assert.expect(4);
	let done = assert.async();

	dataent.run_serially([
		() => {
			return dataent.tests.make('Purchase Order', [
				{supplier: 'Test Supplier'},
				{is_subcontracted: 'No'},
				{buying_price_list: 'Test-Buying-EUR'},
				{currency: 'EUR'},
				{items: [
					[
						{"item_code": 'Test Product 4'},
						{"qty": 5},
						{"uom": 'Unit'},
						{"schedule_date": dataent.datetime.add_days(dataent.datetime.now_date(), 1)},
						{"expected_delivery_date": dataent.datetime.add_days(dataent.datetime.now_date(), 5)},
						{"warehouse": 'Stores - '+dataent.get_abbr(dataent.defaults.get_default("Company"))},
						{"discount_percentage": 20}
					]
				]}
			]);
		},

		() => dataent.timeout(1),

		() => {
			assert.ok(cur_frm.doc.supplier_name == 'Test Supplier', "Supplier name correct");
			assert.ok(cur_frm.doc.items[0].discount_percentage == 20, "Discount correct");
			// Calculate totals after discount
			assert.ok(cur_frm.doc.total == 2000, "Total correct");
			assert.ok(cur_frm.doc.grand_total == 2000, "Grand total correct");
		},

		() => dataent.tests.click_button('Submit'),
		() => dataent.tests.click_button('Yes'),
		() => dataent.timeout(0.3),

		() => done()
	]);
});