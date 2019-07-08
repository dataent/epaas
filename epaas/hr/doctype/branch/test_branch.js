QUnit.module('hr');

QUnit.test("Test: Branch [HR]", function (assert) {
	assert.expect(1);
	let done = assert.async();

	dataent.run_serially([
		// test branch creation
		() => dataent.set_route("List", "Branch", "List"),
		() => dataent.new_doc("Branch"),
		() => dataent.timeout(1),
		() => dataent.quick_entry.dialog.$wrapper.find('.edit-full').click(),
		() => dataent.timeout(1),
		() => cur_frm.set_value("branch", "Test Branch"),

		// save form
		() => cur_frm.save(),
		() => dataent.timeout(1),
		() => assert.equal("Test Branch", cur_frm.doc.branch,
			'name of branch correctly saved'),
		() => done()
	]);
});