QUnit.module('Payment Entry');

QUnit.test("test payment entry", function(assert) {
	assert.expect(6);
	let done = assert.async();
	dataent.run_serially([
		() => {
			return dataent.tests.make('Sales Invoice', [
				{customer: 'Test Customer 1'},
				{items: [
					[
						{'item_code': 'Test Product 1'},
						{'qty': 1},
						{'rate': 101},
					]
				]}
			]);
		},
		() => cur_frm.save(),
		() => dataent.tests.click_button('Submit'),
		() => dataent.tests.click_button('Yes'),
		() => dataent.timeout(1),
		() => dataent.tests.click_button('Close'),
		() => dataent.timeout(1),
		() => dataent.click_button('Make'),
		() => dataent.timeout(1),
		() => dataent.click_link('Payment'),
		() => dataent.timeout(2),
		() => {
			assert.equal(dataent.get_route()[1], 'Payment Entry',
				'made payment entry');
			assert.equal(cur_frm.doc.party, 'Test Customer 1',
				'customer set in payment entry');
			assert.equal(cur_frm.doc.paid_amount, 101,
				'paid amount set in payment entry');
			assert.equal(cur_frm.doc.references[0].allocated_amount, 101,
				'amount allocated against sales invoice');
		},
		() => dataent.timeout(1),
		() => cur_frm.set_value('paid_amount', 100),
		() => dataent.timeout(1),
		() => {
			dataent.model.set_value("Payment Entry Reference", cur_frm.doc.references[0].name,
				"allocated_amount", 101);
		},
		() => dataent.timeout(1),
		() => dataent.click_button('Write Off Difference Amount'),
		() => dataent.timeout(1),
		() => {
			assert.equal(cur_frm.doc.difference_amount, 0, 'difference amount is zero');
			assert.equal(cur_frm.doc.deductions[0].amount, 1, 'Write off amount = 1');
		},
		() => done()
	]);
});
