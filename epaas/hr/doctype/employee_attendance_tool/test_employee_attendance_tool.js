QUnit.module('hr');

QUnit.test("Test: Employee attendance tool [HR]", function (assert) {
	assert.expect(2);
	let done = assert.async();
	let today_date = dataent.datetime.nowdate();
	let date_of_attendance = dataent.datetime.add_days(today_date, -2);	// previous day

	dataent.run_serially([
		// create employee
		() => {
			return dataent.tests.make('Employee', [
				{salutation: "Mr"},
				{employee_name: "Test Employee 2"},
				{company: "For Testing"},
				{date_of_joining: dataent.datetime.add_months(today_date, -2)},	// joined 2 month from now
				{date_of_birth: dataent.datetime.add_months(today_date, -240)},	// age is 20 years
				{employment_type: "Test Employment type"},
				{holiday_list: "Test Holiday list"},
				{branch: "Test Branch"},
				{department: "Test Department"},
				{designation: "Test Designation"}
			]);
		},
		() => dataent.set_route("Form", "Employee Attendance Tool"),
		() => dataent.timeout(0.5),
		() => assert.equal("Employee Attendance Tool", cur_frm.doctype,
			"Form for Employee Attendance Tool opened successfully."),
		// set values in form
		() => cur_frm.set_value("date", date_of_attendance),
		() => cur_frm.set_value("branch", "Test Branch"),
		() => cur_frm.set_value("department", "Test Department"),
		() => cur_frm.set_value("company", "For Testing"),
		() => dataent.timeout(1),
		() => dataent.click_button('Check all'),
		() => dataent.click_button('Mark Present'),
		// check if attendance is marked
		() => dataent.set_route("List", "Attendance", "List"),
		() => dataent.timeout(1),
		() => {
			return dataent.call({
				method: "dataent.client.get_list",
				args: {
					doctype: "Employee",
					filters: {
						"branch": "Test Branch",
						"department": "Test Department",
						"company": "For Testing",
						"status": "Active"
					}
				},
				callback: function(r) {
					let marked_attendance = cur_list.data.filter(d => d.attendance_date == date_of_attendance);
					assert.equal(marked_attendance.length, r.message.length,
						'all the attendance are marked for correct date');
				}
			});
		},
		() => done()
	]);
});