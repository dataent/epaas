QUnit.module('hr');

QUnit.test("Test: Attendance [HR]", function (assert) {
	assert.expect(4);
	let done = assert.async();

	dataent.run_serially([
		// test attendance creation for one employee
		() => dataent.set_route("List", "Attendance", "List"),
		() => dataent.timeout(0.5),
		() => dataent.new_doc("Attendance"),
		() => dataent.timeout(1),
		() => assert.equal("Attendance", cur_frm.doctype,
			"Form for new Attendance opened successfully."),
		// set values in form
		() => cur_frm.set_value("company", "For Testing"),
		() => {
			dataent.db.get_value('Employee', {'employee_name':'Test Employee 1'}, 'name', function(r) {
				cur_frm.set_value("employee", r.name)
			});
		},
		() => dataent.timeout(1),
		() => cur_frm.save(),
		() => dataent.timeout(1),
		// check docstatus of attendance before submit [Draft]
		() => assert.equal("0", cur_frm.doc.docstatus,
			"attendance is currently drafted"),
		// check docstatus of attendance after submit [Present]
		() => cur_frm.savesubmit(),
		() => dataent.timeout(0.5),
		() => dataent.click_button('Yes'),
		() => assert.equal("1", cur_frm.doc.docstatus,
			"attendance is saved after submit"),
		// check if auto filled date is present day
		() => assert.equal(dataent.datetime.nowdate(), cur_frm.doc.attendance_date,
			"attendance for Present day is marked"),
		() => done()
	]);
});