QUnit.module('hr');

QUnit.test("Test: Training Feedback [HR]", function (assert) {
	assert.expect(3);
	let done = assert.async();
	let employee_name;

	dataent.run_serially([
		// Creating Training Feedback
		() => dataent.set_route('List','Training Feedback','List'),
		() => dataent.timeout(0.3),
		() => dataent.click_button('Make a new Training Feedback'),
		() => dataent.timeout(1),
		() => dataent.db.get_value('Employee', {'employee_name': 'Test Employee 1'}, 'name'),
		(r) => {
			employee_name = r.message.name;
		},
		() => cur_frm.set_value('employee',employee_name),
		() => cur_frm.set_value('employee_name','Test Employee 1'),
		() => cur_frm.set_value('training_event','Test Training Event 1'),
		() => cur_frm.set_value('event_name','Test Training Event 1'),
		() => cur_frm.set_value('feedback','Great Experience. This is just a test.'),
		() => dataent.timeout(1),
		() => cur_frm.save(),
		() => dataent.timeout(1),
		() => cur_frm.save(),

		// Submitting the feedback
		() => dataent.click_button('Submit'),
		() => dataent.click_button('Yes'),
		() => dataent.timeout(3),

		// Checking if the feedback is given by correct employee
		() => {
			assert.equal('Test Employee 1',cur_frm.get_field('employee_name').value,
				'Feedback is given by correct employee');

			assert.equal('Test Training Event 1',cur_frm.get_field('training_event').value,
				'Feedback is given for correct event');
		},

		() => dataent.set_route('List','Training Feedback','List'),
		() => dataent.timeout(2),

		// Checking the submission of Training Result
		() => {
			assert.ok(cur_list.data[0].docstatus==1,'Training Feedback Submitted successfully');
		},
		() => done()
	]);
});

