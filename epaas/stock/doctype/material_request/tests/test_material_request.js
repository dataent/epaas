QUnit.module('Stock');

QUnit.test("test material request", function(assert) {
	assert.expect(5);
	let done = assert.async();
	dataent.run_serially([
		() => {
			return dataent.tests.make('Material Request', [
				{items: [
					[
						{'schedule_date':  dataent.datetime.add_days(dataent.datetime.nowdate(), 5)},
						{'qty': 5},
						{'item_code': 'Test Product 1'},
					],
					[
						{'schedule_date':  dataent.datetime.add_days(dataent.datetime.nowdate(), 6)},
						{'qty': 2},
						{'item_code': 'Test Product 2'},
					]
				]},
			]);
		},
		() => cur_frm.save(),
		() => {
			assert.ok(cur_frm.doc.schedule_date == dataent.datetime.add_days(dataent.datetime.now_date(), 5), "Schedule Date correct");

			// get_item_details
			assert.ok(cur_frm.doc.items[0].item_name=='Test Product 1', "Item name correct");
			assert.ok(cur_frm.doc.items[0].schedule_date == dataent.datetime.add_days(dataent.datetime.now_date(), 5), "Schedule Date correct");

			assert.ok(cur_frm.doc.items[1].item_name=='Test Product 2', "Item name correct");
			assert.ok(cur_frm.doc.items[1].schedule_date == dataent.datetime.add_days(dataent.datetime.now_date(), 6), "Schedule Date correct");
		},
		() => dataent.tests.click_button('Submit'),
		() => dataent.tests.click_button('Yes'),
		() => dataent.timeout(0.3),
		() => done()
	]);
});

