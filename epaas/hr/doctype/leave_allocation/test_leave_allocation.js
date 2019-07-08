QUnit.module('hr');

QUnit.test("Test: Leave allocation [HR]", function (assert) {
	assert.expect(3);
	let done = assert.async();
	let today_date = dataent.datetime.nowdate();

	dataent.run_serially([
		// test creating leave alloction
		() => dataent.set_route("List", "Leave Allocation", "List"),
		() => dataent.new_doc("Leave Allocation"),
		() => dataent.timeout(1),
		() => {
			dataent.db.get_value('Employee', {'employee_name':'Test Employee 1'}, 'name', function(r) {
				cur_frm.set_value("employee", r.name)
			});
		},
		() => dataent.timeout(1),
		() => cur_frm.set_value("leave_type", "Test Leave type"),
		() => cur_frm.set_value("to_date", dataent.datetime.add_months(today_date, 2)),	// for two months
		() => cur_frm.set_value("description", "This is just for testing"),
		() => cur_frm.set_value("new_leaves_allocated", 2),
		() => dataent.click_check('Add unused leaves from previous allocations'),
		// save form
		() => cur_frm.save(),
		() => dataent.timeout(1),
		() => cur_frm.savesubmit(),
		() => dataent.timeout(1),
		() => assert.equal("Confirm", cur_dialog.title,
			'confirmation for leave alloction shown'),
		() => dataent.click_button('Yes'),
		() => dataent.timeout(1),
		// check auto filled from date
		() => assert.equal(today_date, cur_frm.doc.from_date,
			"from date correctly set"),
		// check for total leaves
		() => assert.equal(cur_frm.doc.carry_forwarded_leaves + 2, cur_frm.doc.total_leaves_allocated,
			"total leave calculation is correctly set"),
		() => done()
	]);
});