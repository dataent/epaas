// Testing Attendance Module in Education
QUnit.module('education');

QUnit.test('Test: Student Leave Application', function(assert){
	assert.expect(4);
	let done = assert.async();
	let student_code;
	let leave_code;
	dataent.run_serially([
		() => dataent.db.get_value('Student', {'student_email_id': 'test2@testmail.com'}, 'name'),
		(student) => {student_code = student.message.name;}, // fetching student code from db

		() => {
			return dataent.tests.make('Student Leave Application', [
				{student: student_code},
				{from_date: '2017-08-02'},
				{to_date: '2017-08-04'},
				{mark_as_present: 0},
				{reason: "Sick Leave."}
			]);
		},
		() => dataent.tests.click_button('Submit'), // Submitting the leave application
		() => dataent.timeout(0.7),
		() => dataent.tests.click_button('Yes'),
		() => dataent.timeout(0.7),
		() => {
			assert.equal(cur_frm.doc.docstatus, 1, "Submitted leave application");
			leave_code = dataent.get_route()[2];
		},
		() => dataent.tests.click_button('Cancel'), // Cancelling the leave application
		() => dataent.timeout(0.7),
		() => dataent.tests.click_button('Yes'),
		() => dataent.timeout(1),
		() => {assert.equal(cur_frm.doc.docstatus, 2, "Cancelled leave application");},
		() => dataent.tests.click_button('Amend'), // Amending the leave application
		() => dataent.timeout(1),
		() => {
			cur_frm.doc.mark_as_present = 1;
			cur_frm.save();
		},
		() => dataent.timeout(0.7),
		() => dataent.tests.click_button('Submit'),
		() => dataent.timeout(0.7),
		() => dataent.tests.click_button('Yes'),
		() => dataent.timeout(0.7),
		() => {assert.equal(cur_frm.doc.amended_from, leave_code, "Amended successfully");},

		() => dataent.timeout(0.5),
		() => {
			return dataent.tests.make('Student Leave Application', [
				{student: student_code},
				{from_date: '2017-08-07'},
				{to_date: '2017-08-09'},
				{mark_as_present: 0},
				{reason: "Sick Leave."}
			]);
		},
		() => dataent.tests.click_button('Submit'),
		() => dataent.timeout(0.7),
		() => dataent.tests.click_button('Yes'),
		() => dataent.timeout(0.7),
		() => {
			assert.equal(cur_frm.doc.docstatus, 1, "Submitted leave application");
			leave_code = dataent.get_route()[2];
		},

		() => done()
	]);
});