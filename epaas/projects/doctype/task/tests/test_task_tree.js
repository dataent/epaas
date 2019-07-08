/* eslint-disable */
// rename this file from _test_[name] to test_[name] to activate
// and remove above this line

QUnit.test("test: Task Tree", function (assert) {
	let done = assert.async();

	// number of asserts
	assert.expect(4);

	dataent.run_serially([
		// insert a new Task
		() => dataent.set_route('Tree', 'Task'),
		() => dataent.timeout(0.5),

		// Checking adding child without selecting any Node
		() => dataent.tests.click_button('New'),
		() => dataent.timeout(0.5),
		() => {assert.equal($(`.msgprint`).text(), "Select a group node first.", "Error message success");},
		() => dataent.tests.click_button('Close'),
		() => dataent.timeout(0.5),

		// Creating child nodes
		() => dataent.tests.click_link('All Tasks'),
		() => dataent.map_group.make('Test-1'),
		() => dataent.map_group.make('Test-3', 1),
		() => dataent.timeout(1),
		() => dataent.tests.click_link('Test-3'),
		() => dataent.map_group.make('Test-4', 0),

		// Checking Edit button
		() => dataent.timeout(0.5),
		() => dataent.tests.click_link('Test-1'),
		() => dataent.tests.click_button('Edit'),
		() => dataent.timeout(1),
		() => dataent.db.get_value('Task', {'subject': 'Test-1'}, 'name'),
		(task) => {assert.deepEqual(dataent.get_route(), ["Form", "Task", task.message.name], "Edit route checks");},

		// Deleting child Node
		() => dataent.set_route('Tree', 'Task'),
		() => dataent.timeout(0.5),
		() => dataent.tests.click_link('Test-1'),
		() => dataent.tests.click_button('Delete'),
		() => dataent.timeout(0.5),
		() => dataent.tests.click_button('Yes'),

		// Deleting Group Node that has child nodes in it
		() => dataent.timeout(0.5),
		() => dataent.tests.click_link('Test-3'),
		() => dataent.tests.click_button('Delete'),
		() => dataent.timeout(0.5),
		() => dataent.tests.click_button('Yes'),
		() => dataent.timeout(1),
		() => {assert.equal(cur_dialog.title, 'Message', 'Error thrown correctly');},
		() => dataent.tests.click_button('Close'),

		// Add multiple child tasks
		() => dataent.tests.click_link('Test-3'),
		() => dataent.timeout(0.5),
		() => dataent.click_button('Add Multiple'),
		() => dataent.timeout(1),
		() => cur_dialog.set_value('tasks', 'Test-6\nTest-7'),
		() => dataent.timeout(0.5),
		() => dataent.click_button('Submit'),
		() => dataent.timeout(2),
		() => dataent.click_button('Expand All'),
		() => dataent.timeout(1),
		() => {
			let count = $(`a:contains("Test-6"):visible`).length + $(`a:contains("Test-7"):visible`).length;
			assert.equal(count, 2, "Multiple Tasks added successfully");
		},

		() => done()
	]);
});

dataent.map_group = {
	make:function(subject, is_group = 0){
		return dataent.run_serially([
			() => dataent.click_button('Add Child'),
			() => dataent.timeout(1),
			() => cur_dialog.set_value('is_group', is_group),
			() => cur_dialog.set_value('subject', subject),
			() => dataent.click_button('Create New'),
			() => dataent.timeout(1.5)
		]);
	}
};
