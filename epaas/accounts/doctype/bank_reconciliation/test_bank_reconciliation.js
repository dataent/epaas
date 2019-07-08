QUnit.module('Account');

QUnit.test("test Bank Reconciliation", function(assert) {
	assert.expect(0);
	let done = assert.async();
	dataent.run_serially([
		() => dataent.set_route('Form', 'Bank Reconciliation'),
		() => cur_frm.set_value('bank_account','Cash - FT'),
		() => dataent.click_button('Get Payment Entries'),
		() => {
			for(var i=0;i<=cur_frm.doc.payment_entries.length-1;i++){
				cur_frm.doc.payment_entries[i].clearance_date = dataent.datetime.add_days(dataent.datetime.now_date(), 2);
			}
		},
		() => {cur_frm.refresh_fields('payment_entries');},
		() => dataent.click_button('Update Clearance Date'),
		() => dataent.timeout(0.5),
		() => dataent.click_button('Close'),
		() => done()
	]);
});

