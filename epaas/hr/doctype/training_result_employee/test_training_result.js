QUnit.module('hr');

QUnit.test("Test: Training Result [HR]", function (assert) {
	assert.expect(5);
	let done = assert.async();
	dataent.run_serially([
		// Creating Training Result
		() => dataent.set_route('List','Training Result','List'),
		() => dataent.timeout(0.3),
		() => dataent.click_button('Make a new Training Result'),
		() => {
			cur_frm.set_value('training_event','Test Training Event 1');
		},
		() => dataent.timeout(1),
		() => dataent.model.set_value('Training Result Employee','New Training Result Employee 1','hours',4),
		() => dataent.model.set_value('Training Result Employee','New Training Result Employee 1','grade','A'),
		() => dataent.model.set_value('Training Result Employee','New Training Result Employee 1','comments','Nice Seminar'),
		() => dataent.timeout(1),
		() => cur_frm.save(),
		() => dataent.timeout(1),
		() => cur_frm.save(),

		// Submitting the Training Result
		() => dataent.click_button('Submit'),
		() => dataent.click_button('Yes'),
		() => dataent.timeout(4),

		// Checking if the fields are correctly set
		() => {
			assert.equal('Test Training Event 1',cur_frm.get_field('training_event').value,
				'Training Result is created');

			assert.equal('Test Employee 1',cur_frm.doc.employees[0].employee_name,
				'Training Result is created for correct employee');

			assert.equal(4,cur_frm.doc.employees[0].hours,
				'Hours field is correctly calculated');

			assert.equal('A',cur_frm.doc.employees[0].grade,
				'Grade field is correctly set');
		},

		() => dataent.set_route('List','Training Result','List'),
		() => dataent.timeout(2),

		// Checking the submission of Training Result
		() => {
			assert.ok(cur_list.data[0].docstatus==1,'Training Result Submitted successfully');
		},
		() => done()
	]);
});

