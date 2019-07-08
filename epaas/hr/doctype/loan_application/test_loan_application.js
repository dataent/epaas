QUnit.module('hr');

QUnit.test("Test: Loan Application [HR]", function (assert) {
	assert.expect(8);
	let done = assert.async();
	let employee_name;

	dataent.run_serially([
		//  Creation of Loan Application
		() => dataent.db.get_value('Employee', {'employee_name': 'Test Employee 1'}, 'name'),
		(r) => {
			employee_name = r.message.name;
		},
		() => {
			return dataent.tests.make('Loan Application', [
				{ company: 'For Testing'},
				{ applicant: employee_name},
				{ applicant_name: 'Test Employee 1'},
				{ status: 'Approved'},
				{ loan_type: 'Test Loan '},
				{ loan_amount: 200000},
				{ description: 'This is just a test'},
				{ repayment_method: 'Repay Over Number of Periods'},
				{ repayment_periods: 24},
				{ rate_of_interest: 14}
			]);
		},
		() => dataent.timeout(6),
		() => dataent.click_button('Submit'),
		() => dataent.timeout(1),
		() => dataent.click_button('Yes'),
		() => dataent.timeout(2),
		() => {
			// To check if all the amounts are correctly calculated

			assert.ok(cur_frm.get_field('applicant_name').value == 'Test Employee 1',
				'Application created successfully');

			assert.ok(cur_frm.get_field('status').value=='Approved',
				'Status of application is correctly set');

			assert.ok(cur_frm.get_field('loan_type').value=='Test Loan',
				'Application is created for correct Loan Type');

			assert.ok(cur_frm.get_field('status').value=='Approved',
				'Status of application is correctly set');

			assert.ok(cur_frm.get_field('repayment_amount').value==9603,
				'Repayment amount is correctly calculated');

			assert.ok(cur_frm.get_field('total_payable_interest').value==30459,
				'Interest amount is correctly calculated');

			assert.ok(cur_frm.get_field('total_payable_amount').value==230459,
				'Total payable amount is correctly calculated');
		},

		() => dataent.set_route('List','Loan Application','List'),
		() => dataent.timeout(2),

		// Checking the submission of Loan Application
		() => {
			assert.ok(cur_list.data[0].docstatus==1,'Loan Application submitted successfully');
		},
		() => dataent.timeout(1),
		() => done()
	]);
});