/* eslint-disable */
// rename this file from _test_[name] to test_[name] to activate
// and remove above this line

QUnit.test("test: Fees", function (assert) {
	let done = assert.async();

	// number of asserts
	assert.expect(1);

	dataent.run_serially('Fees', [

		// insert a new Fees
		() => {
			return dataent.tests.make('Fees', [
				{student: 'STUD00001'},
				{due_date: dataent.datetime.get_today()},
				{fee_structure: 'FS00001'}
			]);
		},
		() => {
			assert.equal(cur_frm.doc.grand_total===cur_frm.doc.outstanding_amount);
		},
		() => dataent.timeout(0.3),
		() => cur_frm.save(),
		() => dataent.tests.click_button('Submit'),
		() => dataent.tests.click_button('Yes'),
		() => done()
	]);

});
