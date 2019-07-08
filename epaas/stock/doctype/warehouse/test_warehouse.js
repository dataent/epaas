QUnit.test("test: warehouse", function (assert) {
	assert.expect(0);
	let done = assert.async();

	dataent.run_serially([
		// test warehouse creation
		() => dataent.set_route("List", "Warehouse"),

		// Create a Laptop Scrap Warehouse
		() => dataent.tests.make(
			"Warehouse", [
				{warehouse_name: "Laptop Scrap Warehouse"},
				{company: "For Testing"}
			]
		),

		() => done()
	]);
});