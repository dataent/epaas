QUnit.test("test: work order", function (assert) {
	assert.expect(25);
	let done = assert.async();
	let laptop_quantity = 5;
	let items = ["CPU", "Keyboard", "Screen"];
	let operation_items = ["CPU", "Keyboard", "Screen"];
	let click_make = () => {
		let element = $(`.btn-primary:contains("Make"):visible`);
		if(!element.length) {
			throw `did not find any button containing 'Make'`;
		}
		element.click();
		return dataent.timeout(1);
	};

	dataent.run_serially([
		// test work order
		() => dataent.set_route("List", "Work Order", "List"),
		() => dataent.timeout(3),

		// Create a laptop work order
		() => {
			return dataent.tests.make('Work Order', [
				{production_item: 'Laptop'},
				{company: 'For Testing'},
				{qty: laptop_quantity},
				{scrap_warehouse: "Laptop Scrap Warehouse - FT"},
				{wip_warehouse: "Work In Progress - FT"},
				{fg_warehouse: "Finished Goods - FT"}
			]);
		},
		() => dataent.timeout(3),
		() => {
			assert.equal(cur_frm.doc.planned_operating_cost, cur_frm.doc.total_operating_cost,
				"Total and Planned Cost is equal");
			assert.equal(cur_frm.doc.planned_operating_cost, cur_frm.doc.total_operating_cost,
				"Total and Planned Cost is equal");

			items.forEach(function(item, index) {
				assert.equal(item, cur_frm.doc.required_items[index].item_code, `Required item ${item} added`);
				assert.equal("Stores - FT", cur_frm.doc.required_items[index].source_warehouse, `Item ${item} warhouse verified`);
				assert.equal("5", cur_frm.doc.required_items[index].required_qty, `Item ${item} quantity verified`);
			});

			operation_items.forEach(function(operation_item, index) {
				assert.equal(`Assemble ${operation_item}`, cur_frm.doc.operations[index].operation,
					`Operation ${operation_item} added`);
				assert.equal(`${operation_item} assembly workstation`, cur_frm.doc.operations[index].workstation,
					`Workstation ${operation_item} linked`);
			});
		},

		// Submit the work order
		() => cur_frm.savesubmit(),
		() => dataent.timeout(1),
		() => dataent.click_button('Yes'),
		() => dataent.timeout(2.5),

		// Confirm the work order timesheet, save and submit it
		() => dataent.click_link("TS-00"),
		() => dataent.timeout(1),
		() => dataent.click_button("Submit"),
		() => dataent.timeout(1),
		() => dataent.click_button("Yes"),
		() => dataent.timeout(2.5),

		// Start the work order process
		() => dataent.set_route("List", "Work Order", "List"),
		() => dataent.timeout(2),
		() => dataent.click_link("Laptop"),
		() => dataent.timeout(1),
		() => dataent.click_button("Start"),
		() => dataent.timeout(0.5),
		() => click_make(),
		() => dataent.timeout(1),
		() => dataent.click_button("Save"),
		() => dataent.timeout(0.5),

		() => {
			assert.equal(cur_frm.doc.total_outgoing_value, cur_frm.doc.total_incoming_value,
				"Total incoming and outgoing cost is equal");
			assert.equal(cur_frm.doc.total_outgoing_value, "99000",
				"Outgoing cost is correct"); // Price of each item x5
		},
		// Submit for work
		() => dataent.click_button("Submit"),
		() => dataent.timeout(0.5),
		() => dataent.click_button("Yes"),
		() => dataent.timeout(0.5),

		// Finish the work order by sending for manufacturing
		() => dataent.set_route("List", "Work Order"),
		() => dataent.timeout(1),
		() => dataent.click_link("Laptop"),
		() => dataent.timeout(1),

		() => {
			assert.ok(dataent.tests.is_visible("5 items in progress", 'p'), "Work order initiated");
			assert.ok(dataent.tests.is_visible("Finish"), "Finish button visible");
		},

		() => dataent.click_button("Finish"),
		() => dataent.timeout(0.5),
		() => click_make(),
		() => {
			assert.equal(cur_frm.doc.total_incoming_value, "105700",
				"Incoming cost is correct "+cur_frm.doc.total_incoming_value); // Price of each item x5, values are in INR
			assert.equal(cur_frm.doc.total_outgoing_value, "99000",
				"Outgoing cost is correct"); // Price of each item x5, values are in INR
			assert.equal(cur_frm.doc.total_incoming_value - cur_frm.doc.total_outgoing_value, cur_frm.doc.value_difference,
				"Value difference is correct"); // Price of each item x5, values are in INR
		},
		() => dataent.click_button("Save"),
		() => dataent.timeout(1),
		() => dataent.click_button("Submit"),
		() => dataent.timeout(1),
		() => dataent.click_button("Yes"),
		() => dataent.timeout(1),

		// Manufacturing finished
		() => dataent.set_route("List", "Work Order", "List"),
		() => dataent.timeout(1),
		() => dataent.click_link("Laptop"),
		() => dataent.timeout(1),

		() => assert.ok(dataent.tests.is_visible("5 items produced", 'p'), "Work order completed"),

		() => done()
	]);
});
