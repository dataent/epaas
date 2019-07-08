QUnit.module('hr');

QUnit.test("Test: Job Offer [HR]", function (assert) {
	assert.expect(3);
	let done = assert.async();
	dataent.run_serially([
		// Job Offer Creation
		() => {
			dataent.tests.make('Job Offer', [
				{ job_applicant: 'Utkarsh Goswami - goswamiutkarsh0@gmail.com - software-developer'},
				{ applicant_name: 'Utkarsh Goswami'},
				{ status: 'Accepted'},
				{ designation: 'Software Developer'},
				{ offer_terms: [
					[
						{offer_term: 'Responsibilities'},
						{value: 'Design, installation, testing and maintenance of software systems.'}
					],
					[
						{offer_term: 'Department'},
						{value: 'Research & Development'}
					],
					[
						{offer_term: 'Probationary Period'},
						{value: 'The Probation period is for 3 months.'}
					]
				]},
			]);
		},
		() => dataent.timeout(10),
		() => dataent.click_button('Submit'),
		() => dataent.timeout(2),
		() => dataent.click_button('Yes'),
		() => dataent.timeout(5),
		// To check if the fields are correctly set
		() => {
			assert.ok(cur_frm.get_field('status').value=='Accepted',
				'Status of job offer is correct');
			assert.ok(cur_frm.get_field('designation').value=='Software Developer',
				'Designation of applicant is correct');
		},
		() => dataent.set_route('List','Job Offer','List'),
		() => dataent.timeout(2),
		// Checking the submission of and Job Offer
		() => {
			assert.ok(cur_list.data[0].docstatus==1,'Job Offer Submitted successfully');
		},
		() => dataent.timeout(2),
		() => done()
	]);
});