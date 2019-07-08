QUnit.module('hr');

QUnit.test("Test: Expense Claim [HR]", function (assert) {
	assert.expect(3);
	let done = assert.async();
	let employee_name;

	dataent.run_serially([
		// Creating Appraisal
		() => dataent.set_route('List','Appraisal','List'),
		() => dataent.timeout(0.3),
		() => dataent.click_button('Make a new Appraisal'),
		() => {
			cur_frm.set_value('kra_template','Test Appraisal 1'),
			cur_frm.set_value('start_date','2017-08-21'),
			cur_frm.set_value('end_date','2017-09-21');
		},
		() => dataent.timeout(1),
		() => dataent.model.set_value('Appraisal Goal','New Appraisal Goal 1','score',4),
		() => dataent.model.set_value('Appraisal Goal','New Appraisal Goal 1','score_earned',2),
		() => dataent.model.set_value('Appraisal Goal','New Appraisal Goal 2','score',4),
		() => dataent.model.set_value('Appraisal Goal','New Appraisal Goal 2','score_earned',2),
		() => dataent.timeout(1),
		() => dataent.db.get_value('Employee', {'employee_name': 'Test Employee 1'}, 'name'),
		(r) => {
			employee_name = r.message.name;
		},

		() => dataent.timeout(1),
		() => cur_frm.set_value('employee',employee_name),
		() => cur_frm.set_value('employee_name','Test Employee 1'),
		() => cur_frm.set_value('company','For Testing'),
		() => dataent.click_button('Calculate Total Score'),
		() => dataent.timeout(1),
		() => cur_frm.save(),
		() => dataent.timeout(1),
		() => cur_frm.save(),

		// Submitting the Appraisal
		() => dataent.click_button('Submit'),
		() => dataent.click_button('Yes'),
		() => dataent.timeout(3),

		// Checking if the appraisal is correctly set for the employee
		() => {
			assert.equal('Submitted',cur_frm.get_field('status').value,
				'Appraisal is submitted');

			assert.equal('Test Employee 1',cur_frm.get_field('employee_name').value,
				'Appraisal is created for correct employee');

			assert.equal(4,cur_frm.get_field('total_score').value,
				'Total score is correctly calculated');
		},
		() => done()
	]);
});

