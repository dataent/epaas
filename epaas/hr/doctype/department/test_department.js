QUnit.module('hr');

QUnit.test("Test: Department [HR]", function (assert) {
	assert.expect(1);
	let done = assert.async();

	dataent.run_serially([
		// test department creation
		() => dataent.set_route("List", "Department", "List"),
		() => dataent.new_doc("Department"),
		() => dataent.timeout(1),
		() => dataent.quick_entry.dialog.$wrapper.find('.edit-full').click(),
		() => dataent.timeout(1),
		() => cur_frm.set_value("department_name", "Test Department"),
		() => cur_frm.set_value("leave_block_list", "Test Leave block list"),
		// save form
		() => cur_frm.save(),
		() => dataent.timeout(1),
		() => assert.equal("Test Department", cur_frm.doc.department_name,
			'name of department correctly saved'),
		() => done()
	]);
});