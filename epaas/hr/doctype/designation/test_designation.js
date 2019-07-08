QUnit.module('hr');

QUnit.test("Test: Designation [HR]", function (assert) {
	assert.expect(1);
	let done = assert.async();

	dataent.run_serially([
		// test designation creation
		() => dataent.set_route("List", "Designation", "List"),
		() => dataent.new_doc("Designation"),
		() => dataent.timeout(1),
		() => dataent.quick_entry.dialog.$wrapper.find('.edit-full').click(),
		() => dataent.timeout(1),
		() => cur_frm.set_value("designation_name", "Test Designation"),
		() => cur_frm.set_value("description", "This designation is just for testing."),
		// save form
		() => cur_frm.save(),
		() => dataent.timeout(1),
		() => assert.equal("Test Designation", cur_frm.doc.designation_name,
			'name of designation correctly saved'),
		() => done()
	]);
});