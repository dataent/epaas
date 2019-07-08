QUnit.module('hr');
QUnit.test("Test: Appraisal Template [HR]", function (assert) {
	assert.expect(1);
	let done = assert.async();
	dataent.run_serially([
		// Job Opening creation
		() => {
			dataent.tests.make('Appraisal Template', [
				{ kra_title: 'Test Appraisal 1'},
				{ description: 'This is just a test'},
				{ goals: [
					[
						{ kra: 'Design'},
						{ per_weightage: 50}
					],
					[
						{ kra: 'Code creation'},
						{ per_weightage: 50}
					]
				]},
			]);
		},
		() => dataent.timeout(10),
		() => {
			assert.equal('Test Appraisal 1',cur_frm.doc.kra_title, 'Appraisal name correctly set');
		},
		() => done()
	]);
});

