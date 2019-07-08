QUnit.module('Admission');

QUnit.test('Make Students', function(assert){
	assert.expect(0);
	let done = assert.async();
	let tasks = [];
	let loop = [1,2,3,4];
	let fname;

	dataent.run_serially([
		// Making School House to be used in this test and later
		() => dataent.set_route('Form', 'School House/New School House'),
		() => dataent.timeout(0.5),
		() => cur_frm.doc.house_name = 'Test_house',
		() => cur_frm.save(),

		// Making Student Applicant entries
		() => {
			loop.forEach(index => {
				tasks.push(() => {
					fname = "Fname" + index;

					return dataent.tests.make('Student Applicant', [
						{first_name: fname},
						{middle_name: "Mname"},
						{last_name: "Lname"},
						{program: "Standard Test"},
						{student_admission: "2016-17 Admissions"},
						{date_of_birth: '1995-08-20'},
						{student_email_id: ('test' + (index+3) + '@testmail.com')},
						{gender: 'Male'},
						{student_mobile_number: (9898980000 + index)},
						{blood_group: 'O+'},
						{address_line_1: 'Test appt, Test Society,'},
						{address_line_2: 'Test district, Test city.'},
						{city: 'Test'},
						{state: 'Test'},
						{pincode: '395007'}
					]);
				});
			});
			return dataent.run_serially(tasks);
		},

		// Using Program Enrollment Tool to enroll all dummy student at once
		() => dataent.set_route('Form', 'Program Enrollment Tool'),
		() => {
			cur_frm.set_value("get_students_from", "Student Applicants");
			cur_frm.set_value("academic_year", "2016-17");
			cur_frm.set_value("program", "Standard Test");
		},
		() => dataent.tests.click_button("Get Students"),
		() => dataent.timeout(1),
		() => dataent.tests.click_button("Enroll Students"),
		() => dataent.timeout(1.5),
		() => dataent.tests.click_button("Close"),

		// Submitting required data for each enrolled Student
		() => {
			tasks = [];
			loop.forEach(index => {
				tasks.push(
					() => {fname = "Fname" + index + " Mname Lname";},
					() => dataent.set_route('List', 'Program Enrollment/List'),
					() => dataent.timeout(0.6),
					() => dataent.tests.click_link(fname),
					() => dataent.timeout(0.4),
					() => {
						cur_frm.set_value('program', 'Standard Test');
						cur_frm.set_value('student_category', 'Reservation');
						cur_frm.set_value('student_batch_name', 'A');
						cur_frm.set_value('academic_year', '2016-17');
						cur_frm.set_value('academic_term', '2016-17 (Semester 1)');
						cur_frm.set_value('school_house', 'Test_house');
					},
					() => cur_frm.save(),
					() => dataent.timeout(0.5),
					() => dataent.tests.click_button('Submit'),
					() => dataent.tests.click_button('Yes'),
					() => dataent.timeout(0.5)
				);
			});
			return dataent.run_serially(tasks);
		},
		() => done()
	]);
});