// Education Assessment module
QUnit.module('education');

QUnit.test('Test: Assessment Group', function(assert){
	assert.expect(4);
	let done = assert.async();

	dataent.run_serially([
		() => dataent.set_route('Tree', 'Assessment Group'),

		// Checking adding child without selecting any Node
		() => dataent.tests.click_button('New'),
		() => dataent.timeout(0.2),
		() => {assert.equal($(`.msgprint`).text(), "Select a group node first.", "Error message success");},
		() => dataent.tests.click_button('Close'),
		() => dataent.timeout(0.2),

		// Creating child nodes
		() => dataent.tests.click_link('All Assessment Groups'),
		() => dataent.map_group.make('Assessment-group-1'),
		() => dataent.map_group.make('Assessment-group-4', "All Assessment Groups", 1),
		() => dataent.tests.click_link('Assessment-group-4'),
		() => dataent.map_group.make('Assessment-group-5', "Assessment-group-3", 0),

		// Checking Edit button
		() => dataent.timeout(0.5),
		() => dataent.tests.click_link('Assessment-group-1'),
		() => dataent.tests.click_button('Edit'),
		() => dataent.timeout(0.5),
		() => {assert.deepEqual(dataent.get_route(), ["Form", "Assessment Group", "Assessment-group-1"], "Edit route checks");},

		// Deleting child Node
		() => dataent.set_route('Tree', 'Assessment Group'),
		() => dataent.timeout(0.5),
		() => dataent.tests.click_link('Assessment-group-1'),
		() => dataent.tests.click_button('Delete'),
		() => dataent.timeout(0.5),
		() => dataent.tests.click_button('Yes'),

		// Checking Collapse and Expand button
		() => dataent.timeout(2),
		() => dataent.tests.click_link('Assessment-group-4'),
		() => dataent.click_button('Collapse'),
		() => dataent.tests.click_link('All Assessment Groups'),
		() => dataent.click_button('Collapse'),
		() => {assert.ok($('.opened').size() == 0, 'Collapsed');},
		() => dataent.click_button('Expand'),
		() => {assert.ok($('.opened').size() > 0, 'Expanded');},

		() => done()
	]);
});

dataent.map_group = {
	make:function(assessment_group_name, parent_assessment_group = 'All Assessment Groups', is_group = 0){
		return dataent.run_serially([
			() => dataent.click_button('Add Child'),
			() => dataent.timeout(0.2),
			() => cur_dialog.set_value('is_group', is_group),
			() => cur_dialog.set_value('assessment_group_name', assessment_group_name),
			() => cur_dialog.set_value('parent_assessment_group', parent_assessment_group),
			() => dataent.click_button('Create New'),
		]);
	}
};