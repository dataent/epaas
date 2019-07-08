/* eslint-disable */
// rename this file from _test_[name] to test_[name] to activate
// and remove above this line

QUnit.test("test: Restaurant Table", function (assert) {
	let done = assert.async();

	// number of asserts
	assert.expect(0);

	dataent.run_serially([
		// insert a new Restaurant Table
		() => dataent.tests.make('Restaurant Table', [
			// values to be set
			{restaurant: 'Test Restaurant 1'},
			{no_of_seats: 4},
		]),
		() => dataent.tests.make('Restaurant Table', [
			// values to be set
			{restaurant: 'Test Restaurant 1'},
			{no_of_seats: 5},
		]),
		() => dataent.tests.make('Restaurant Table', [
			// values to be set
			{restaurant: 'Test Restaurant 1'},
			{no_of_seats: 2},
		]),
		() => dataent.tests.make('Restaurant Table', [
			// values to be set
			{restaurant: 'Test Restaurant 1'},
			{no_of_seats: 2},
		]),
		() => dataent.tests.make('Restaurant Table', [
			// values to be set
			{restaurant: 'Test Restaurant 1'},
			{no_of_seats: 6},
		]),
		() => done()
	]);

});
