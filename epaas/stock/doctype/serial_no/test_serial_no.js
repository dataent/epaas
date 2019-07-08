/* eslint-disable */
// rename this file from _test_[name] to test_[name] to activate
// and remove above this line

QUnit.test("test: Serial No", function (assert) {
	let done = assert.async();

	// number of asserts
	assert.expect(1);

	dataent.run_serially([
		// insert a new Serial No
		() => dataent.tests.make('Serial No', [
			// values to be set
			{key: 'value'}
		]),
		() => {
			assert.equal(cur_frm.doc.key, 'value');
		},
		() => done()
	]);

});
