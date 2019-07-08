QUnit.module('hr');

QUnit.test("Test: Loan Type [HR]", function (assert) {
	assert.expect(3);
	let done = assert.async();

	dataent.run_serially([
		// Loan Type creation
		() => {
			dataent.tests.make('Loan Type', [
				{ loan_name: 'Test Loan'},
				{ maximum_loan_amount: 400000},
				{ rate_of_interest: 14},
				{ description:
					'This is just a test.'}
			]);
		},
		() => dataent.timeout(7),
		() => dataent.set_route('List','Loan Type','List'),
		() => dataent.timeout(4),

		// Checking if the fields are correctly set
		() => {
			assert.ok(cur_list.data.length==1, 'Loan Type created successfully');
			assert.ok(cur_list.data[0].name=='Test Loan', 'Loan title Correctly set');
			assert.ok(cur_list.data[0].disabled==0, 'Loan enabled');
		},
		() => done()
	]);
});

