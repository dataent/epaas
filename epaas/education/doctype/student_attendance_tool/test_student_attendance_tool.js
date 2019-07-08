// Testing Attendance Module in Education
QUnit.module('education');

QUnit.test('Test: Student Attendace Tool', function(assert){
	assert.expect(10);
	let done = assert.async();
	let i, count = 0;

	dataent.run_serially([
		() => dataent.timeout(0.2),
		() => dataent.set_route('Form', 'Student Attendance Tool'),
		() => dataent.timeout(0.5),

		() => {
			if(cur_frm.doc.based_on == 'Student Group' || cur_frm.doc.based_on == 'Course Schedule'){
				cur_frm.doc.based_on = 'Student Group';
				assert.equal(1, 1, 'Attendance basis correctly set');
				cur_frm.set_value("group_based_on", 'Batch');
				cur_frm.set_value("student_group", "test-batch-wise-group");
				cur_frm.set_value("date", dataent.datetime.nowdate());
			}
		},
		() => dataent.timeout(0.5),
		() => {
			assert.equal($('input.students-check').size(), 5, "Student list based on batch correctly fetched");
			assert.equal(dataent.datetime.nowdate(), cur_frm.doc.date, 'Current date correctly set');

			cur_frm.set_value("student_group", "test-batch-wise-group-2");
			assert.equal($('input.students-check').size(), 5, "Student list based on batch 2 correctly fetched");

			cur_frm.set_value("group_based_on", 'Course');

			cur_frm.set_value("student_group", "test-course-wise-group");
			assert.equal($('input.students-check').size(), 5, "Student list based on course correctly fetched");

			cur_frm.set_value("student_group", "test-course-wise-group-2");
			assert.equal($('input.students-check').size(), 5, "Student list based on course 2 correctly fetched");
		},

		() => dataent.timeout(1),
		() => dataent.tests.click_button('Check all'), // Marking all Student as checked
		() => {
			for(i = 0; i < $('input.students-check').size(); i++){
				if($('input.students-check')[i].checked == true)
					count++;
			}

			if(count == $('input.students-check').size())
				assert.equal($('input.students-check').size(), count, "All students marked checked");
		},

		() => dataent.timeout(1),
		() => dataent.tests.click_button('Uncheck all'), // Marking all Student as unchecked
		() => {
			count = 0;
			for(i = 0; i < $('input.students-check').size(); i++){
				if(!($('input.students-check')[i].checked))
					count++;
			}

			if(count == $('input.students-check').size())
				assert.equal($('input.students-check').size(), count, "All students marked checked");
		},

		() => dataent.timeout(1),
		() => dataent.tests.click_button('Check all'),
		() => dataent.tests.click_button('Mark Attendance'),
		() => dataent.timeout(1),
		() => dataent.tests.click_button('Yes'),
		() => dataent.timeout(1),
		() => {
			assert.equal($('.msgprint').text(), "Attendance has been marked successfully.", "Attendance successfully marked");
			dataent.tests.click_button('Close');
		},

		() => dataent.timeout(1),
		() => dataent.set_route('List', 'Student Attendance/List'),
		() => dataent.timeout(1),
		() => {
			assert.equal(cur_list.data.length, count, "Attendance list created");
		},

		() => done()
	]);
});