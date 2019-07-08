QUnit.module('hr');

QUnit.test("Test: Leave block list [HR]", function (assert) {
	assert.expect(1);
	let done = assert.async();
	let today_date = dataent.datetime.nowdate();

	dataent.run_serially([
		// test leave block list creation
		() => dataent.set_route("List", "Leave Block List", "List"),
		() => dataent.new_doc("Leave Block List"),
		() => dataent.timeout(1),
		() => cur_frm.set_value("leave_block_list_name", "Test Leave block list"),
		() => cur_frm.set_value("company", "For Testing"),
		() => dataent.click_button('Add Row'),
		() => {
			cur_frm.fields_dict.leave_block_list_dates.grid.grid_rows[0].doc.block_date = today_date;
			cur_frm.fields_dict.leave_block_list_dates.grid.grid_rows[0].doc.reason = "Blocked leave test";
		},
		// save form
		() => cur_frm.save(),
		() => dataent.timeout(1),
		() => assert.equal("Test Leave block list", cur_frm.doc.leave_block_list_name,
			'name of blocked leave list correctly saved'),
		() => done()
	]);
});