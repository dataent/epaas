QUnit.test("test: Activity Type", function (assert) {
	// number of asserts
	assert.expect(1);
	let done = assert.async();

	dataent.run_serially([
		// insert a new Activity Type
		() => dataent.set_route("List", "Activity Type", "List"),
		() => dataent.new_doc("Activity Type"),
		() => dataent.timeout(1),
		() => dataent.quick_entry.dialog.$wrapper.find('.edit-full').click(),
		() => dataent.timeout(1),
		() => cur_frm.set_value("activity_type", "Test Activity"),
		() => dataent.click_button('Save'),
		() => dataent.timeout(1),
		() => {
			assert.equal(cur_frm.doc.name,"Test Activity");
		},
		() => done()
	]);
});
