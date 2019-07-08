QUnit.module('Stock');

QUnit.test("test material request", function(assert) {
	assert.expect(3);
	let done = assert.async();
	dataent.run_serially([
		() => {
			return dataent.tests.make('Stock Entry', [
				{purpose:'Material Transfer'},
				{from_warehouse:'Stores - '+dataent.get_abbr(dataent.defaults.get_default('Company'))},
				{to_warehouse:'Work In Progress - '+dataent.get_abbr(dataent.defaults.get_default('Company'))},
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
			assert.ok(cur_frm.doc.total_incoming_value==500, " Incoming Value correct");
		},
		() => dataent.tests.click_button('Submit'),
		() => dataent.tests.click_button('Yes'),
		() => dataent.timeout(0.3),
		() => done()
	]);
});

