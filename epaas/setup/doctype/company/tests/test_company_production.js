QUnit.test("Test: Company", function (assert) {
	assert.expect(0);

	let done = assert.async();

	dataent.run_serially([
		// Added company for Work Order testing
		() => dataent.set_route("List", "Company"),
		() => dataent.new_doc("Company"),
		() => dataent.timeout(1),
		() => cur_frm.set_value("company_name", "For Testing"),
		() => cur_frm.set_value("abbr", "RB"),
		() => cur_frm.set_value("default_currency", "INR"),
		() => cur_frm.save(),
		() => dataent.timeout(1),

		() => done()
	]);
});