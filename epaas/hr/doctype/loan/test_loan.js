
QUnit.test("Test Loan [HR]", function(assert) {
	assert.expect(8);
	let done = assert.async();
	let employee_name;

	// To create a loan and check principal,interest and balance amount
	let loan_creation = (ename,lname) => {
		return dataent.run_serially([
			() => dataent.db.get_value('Employee', {'employee_name': ename}, 'name'),
			(r) => {
				employee_name = r.message.name;
			},
			() => dataent.db.get_value('Loan Application', {'loan_type': lname}, 'name'),
			(r) => {
				// Creating loan for an employee
				return dataent.tests.make('Loan', [
					{ company: 'For Testing'},
					{ posting_date: '2017-08-26'},
					{ applicant: employee_name},
					{ loan_application: r.message.name},
					{ disbursement_date: '2018-08-26'},
					{ mode_of_payment: 'Cash'},
					{ loan_account: 'Temporary Opening - FT'},
					{ interest_income_account: 'Service - FT'}
				]);
			},
			() => dataent.timeout(3),
			() => dataent.click_button('Submit'),
			() => dataent.timeout(1),
			() => dataent.click_button('Yes'),
			() => dataent.timeout(3),

			// Checking if all the amounts are correctly calculated
			() => {
				assert.ok(cur_frm.get_field('applicant_name').value=='Test Employee 1'&&
					(cur_frm.get_field('status').value=='Sanctioned'),
				'Loan Sanctioned for correct employee');

				assert.equal(7270,
					cur_frm.get_doc('repayment_schedule').repayment_schedule[0].principal_amount,
					'Principal amount for first instalment is correctly calculated');

				assert.equal(2333,
					cur_frm.get_doc('repayment_schedule').repayment_schedule[0].interest_amount,
					'Interest amount for first instalment is correctly calculated');

				assert.equal(192730,
					cur_frm.get_doc('repayment_schedule').repayment_schedule[0].balance_loan_amount,
					'Balance amount after first instalment is correctly calculated');

				assert.equal(9479,
					cur_frm.get_doc('repayment_schedule').repayment_schedule[23].principal_amount,
					'Principal amount for last instalment is correctly calculated');

				assert.equal(111,
					cur_frm.get_doc('repayment_schedule').repayment_schedule[23].interest_amount,
					'Interest amount for last instalment is correctly calculated');

				assert.equal(0,
					cur_frm.get_doc('repayment_schedule').repayment_schedule[23].balance_loan_amount,
					'Balance amount after last instalment is correctly calculated');

			},
			() => dataent.set_route('List','Loan','List'),
			() => dataent.timeout(2),

			// Checking the submission of Loan
			() => {
				assert.ok(cur_list.data[0].docstatus==1,'Loan sanctioned and submitted successfully');
			},
		]);
	};
	dataent.run_serially([
		// Creating loan
		() => loan_creation('Test Employee 1','Test Loan'),
		() => done()
	]);
});
