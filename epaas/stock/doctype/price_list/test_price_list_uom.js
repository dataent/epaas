QUnit.module('Price List');

QUnit.test("test price list with uom dependancy", function(assert) {
	assert.expect(2);
	let done = assert.async();
	dataent.run_serially([

		() => dataent.set_route('Form', 'Price List', 'Standard Buying'),
		() => {
			cur_frm.set_value('price_not_uom_dependent','1');
			dataent.timeout(1);
		},
		() => cur_frm.save(),

		() => dataent.timeout(1),

		() => {
			return dataent.tests.make('Item Price', [
				{price_list:'Standard Buying'},
				{item_code: 'Test Product 3'},
				{price_list_rate: 200}
			]);
		},

		() => cur_frm.save(),

		() => {
			return dataent.tests.make('Purchase Order', [
				{supplier: 'Test Supplier'},
				{currency: 'INR'},
				{buying_price_list: 'Standard Buying'},
				{items: [
					[
						{"item_code": 'Test Product 3'},
						{"schedule_date": dataent.datetime.add_days(dataent.datetime.now_date(), 2)},
						{"uom": 'Nos'},
						{"conversion_factor": 3}
					]
				]},

			]);
		},

		() => cur_frm.save(),
		() => dataent.timeout(0.3),

		() => {
			assert.ok(cur_frm.doc.items[0].item_name == 'Test Product 3', "Item code correct");
			assert.ok(cur_frm.doc.items[0].price_list_rate == 200, "Price list rate correct");
		},

		() => dataent.tests.click_button('Submit'),
		() => dataent.tests.click_button('Yes'),
		() => dataent.timeout(1),

		() => done()
	]);
});