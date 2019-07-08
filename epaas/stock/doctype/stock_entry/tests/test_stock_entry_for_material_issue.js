QUnit.module('Stock');

QUnit.test("test material request", function(assert) {
	assert.expect(2);
	let done = assert.async();
	dataent.run_serially([
		() => {
			return dataent.tests.make('Stock Entry', [
				{from_warehouse:'Stores - '+dataent.get_abbr(dataent.defaults.get_default('Company'))},
				{items: [
					[
						{'item_code': 'Test Product 1'},
						{'qty': 5},
					]
				]},
			]);
		},
		() => cur_frm.save(),
		() => dataent.click_button('Update Rate and Availability'),
		() => {
			// get_item_details
			assert.ok(cur_frm.doc.items[0].item_name=='Test Product 1', "Item name correct");
			assert.ok(cur_frm.doc.total_outgoing_value==500, " Outgoing Value correct");
		},
		() => dataent.tests.click_button('Submit'),
		() => dataent.tests.click_button('Yes'),
		() => dataent.timeout(0.3),
		() => done()
	]);
});

