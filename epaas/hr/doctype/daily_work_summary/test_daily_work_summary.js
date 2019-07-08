/* eslint-disable */
// rename this file from _test_[name] to test_[name] to activate
// and remove above this line

QUnit.test("test: Daily Work Summary", function (assert) {
	let done = assert.async();

	// number of asserts
	assert.expect(1);

	dataent.run_serially([
		// insert a new Daily Work Summary
		() => dataent.tests.make('Daily Work Summary', [
			// values to be set
			{ key: 'value' }
		]),
		() => {
			assert.equal(cur_frm.doc.key, 'value');
		},
		() => done()
	]);

});