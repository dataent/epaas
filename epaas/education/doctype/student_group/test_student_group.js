// Testing Student Module in Education
QUnit.module('education');

QUnit.test('Test: Student Group', function(assert){
	assert.expect(2);
	let done = assert.async();
	let group_based_on = ["test-batch-wise-group", "test-course-wise-group"];
	let tasks = [];

	dataent.run_serially([
		// Creating a Batch and Course based group
		() => {
			return dataent.tests.make('Student Group', [
				{academic_year: '2016-17'},
				{academic_term: '2016-17 (Semester 1)'},
				{program: "Standard Test"},
				{group_based_on: 'Batch'},
				{student_group_name: group_based_on[0]},
				{max_strength: 10},
				{batch: 'A'}
			]);
		},
		() => {
			return dataent.tests.make('Student Group', [
				{academic_year: '2016-17'},
				{academic_term: '2016-17 (Semester 1)'},
				{program: "Standard Test"},
				{group_based_on: 'Course'},
				{student_group_name: group_based_on[1]},
				{max_strength: 10},
				{batch: 'A'},
				{course: 'Test_Sub'},
			]);
		},

		// Populating the created group with Students
		() => {
			tasks = [];
			group_based_on.forEach(index => {
				tasks.push(
					() => dataent.timeout(0.5),
					() => dataent.set_route("Form", ('Student Group/' + index)),
					() => dataent.timeout(0.5),
					() => dataent.tests.click_button('Get Students'),
					() => dataent.timeout(1),
					() => {
						assert.equal(cur_frm.doc.students.length, 5, 'Successfully fetched list of students');
					},
				);
			});
			return dataent.run_serially(tasks);
		},

		() => done()
	]);
});