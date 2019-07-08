/* eslint-disable */
// rename this file from _test_[name] to test_[name] to activate
// and remove above this line

QUnit.test("test: Location", function (assert) {
	let done = assert.async();

	// number of asserts
	assert.expect(1);

	dataent.run_serially([
		// insert a new Location
		() => dataent.tests.make('Location', [
			// values to be set
			{ location_name: 'Basil Farm' }
		]),
		() => {
			assert.equal(cur_frm.doc.name, 'Basil Farm');
		},
		() => done()
	]);

});
