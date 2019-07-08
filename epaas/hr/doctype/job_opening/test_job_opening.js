QUnit.module('hr');

QUnit.test("Test: Job Opening [HR]", function (assert) {
	assert.expect(2);
	let done = assert.async();

	dataent.run_serially([
		// Job Opening creation
		() => {
			dataent.tests.make('Job Opening', [
				{ job_title: 'Software Developer'},
				{ description:
					'You might be responsible for writing and coding individual'+
					' programmes or providing an entirely new software resource.'}
			]);
		},
		() => dataent.timeout(4),
		() => dataent.set_route('List','Job Opening'),
		() => dataent.timeout(3),
		() => {
			assert.ok(cur_list.data.length==1, 'Job Opening created successfully');
			assert.ok(cur_list.data[0].job_title=='Software Developer', 'Job title Correctly set');
		},
		() => done()
	]);
});

