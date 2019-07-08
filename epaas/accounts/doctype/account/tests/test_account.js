QUnit.module('accounts');

QUnit.test("test account", function(assert) {
	assert.expect(4);
	let done = assert.async();
	dataent.run_serially([
		() => dataent.set_route('Tree', 'Account'),
		() => dataent.timeout(3),
		() => dataent.click_button('Expand All'),
		() => dataent.timeout(1),
		() => dataent.click_link('Debtors'),
		() => dataent.click_button('Edit'),
		() => dataent.timeout(1),
		() => {
			assert.ok(cur_frm.doc.root_type=='Asset');
			assert.ok(cur_frm.doc.report_type=='Balance Sheet');
			assert.ok(cur_frm.doc.account_type=='Receivable');
		},
		() => dataent.click_button('Ledger'),
		() => dataent.timeout(1),
		() => {
			// check if general ledger report shown
			assert.deepEqual(dataent.get_route(), ['query-report', 'General Ledger']);
			window.history.back();
			return dataent.timeout(1);
		},
		() => done()
	]);
});
