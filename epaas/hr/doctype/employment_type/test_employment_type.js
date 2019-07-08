QUnit.module('hr');

QUnit.test("Test: Employment type [HR]", function (assert) {
	assert.expect(1);
	let done = assert.async();

	dataent.run_serially([
		// test employment type creation
		() => dataent.set_route("List", "Employment Type", "List"),
		() => dataent.new_doc("Employment Type"),
		() => dataent.timeout(1),
		() => dataent.quick_entry.dialog.$wrapper.find('.edit-full').click(),
		() => dataent.timeout(1),
		() => cur_frm.set_value("employee_type_name", "Test Employment type"),
		// save form
		() => cur_frm.save(),
		() => dataent.timeout(1),
		() => assert.equal("Test Employment type", cur_frm.doc.employee_type_name,
			'name of employment type correctly saved'),
		() => done()
	]);
});