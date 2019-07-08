QUnit.module('Stock');

QUnit.test("test Batch", function(assert) {
	assert.expect(1);
	let done = assert.async();
	dataent.run_serially([
		() => {
			return dataent.tests.make('Batch', [
				{batch_id:'TEST-BATCH-001'},
				{item:'Test Product 4'},
				{expiry_date:dataent.datetime.add_days(dataent.datetime.now_date(), 2)},
			]);
		},
		() => cur_frm.save(),
		() => {
			// get_item_details
			assert.ok(cur_frm.doc.batch_id=='TEST-BATCH-001', "Batch Id correct");
		},
		() => dataent.timeout(0.3),
		() => done()
	]);
});

