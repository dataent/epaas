/* eslint-disable */
// rename this file from _test_[name] to test_[name] to activate
// and remove above this line

QUnit.test("test: Agriculture Analysis Criteria", function (assert) {
	let done = assert.async();

	// number of asserts
	assert.expect(1);

	dataent.run_serially([
		// insert a new Agriculture Analysis Criteria
		() => dataent.tests.make('Agriculture Analysis Criteria', [
			// values to be set
			{key: 'value'}
		]),
		() => {
			assert.equal(cur_frm.doc.key, 'value');
		},
		() => done()
	]);

});
