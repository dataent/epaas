QUnit.module('hr');

QUnit.test("Test: Leave type [HR]", function (assert) {
	assert.expect(1);
	let done = assert.async();

	dataent.run_serially([
		// test leave type creation
		() => dataent.set_route("List", "Leave Type", "List"),
		() => dataent.new_doc("Leave Type"),
		() => dataent.timeout(1),
		() => cur_frm.set_value("leave_type_name", "Test Leave type"),
		() => cur_frm.set_value("max_continuous_days_allowed", "5"),
		() => dataent.click_check('Is Carry Forward'),
		// save form
		() => cur_frm.save(),
		() => dataent.timeout(1),
		() => assert.equal("Test Leave type", cur_frm.doc.leave_type_name,
			'leave type correctly saved'),
		() => done()
	]);
});