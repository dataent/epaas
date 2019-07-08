QUnit.module('Stock');

QUnit.test("test material request", function(assert) {
	assert.expect(1);
	let done = assert.async();
	dataent.run_serially([
		() => {
			return dataent.tests.make('Material Request', [
				{material_request_type:'Manufacture'},
				{items: [
					[
						{'schedule_date':  dataent.datetime.add_days(dataent.datetime.nowdate(), 5)},
						{'qty': 5},
						{'item_code': 'Test Product 1'},
					]
				]},
			]);
		},
		() => cur_frm.save(),
		() => {
			// get_item_details
			assert.ok(cur_frm.doc.items[0].item_name=='Test Product 1', "Item name correct");
		},
		() => dataent.tests.click_button('Submit'),
		() => dataent.tests.click_button('Yes'),
		() => dataent.timeout(0.3),
		() => done()
	]);
});

