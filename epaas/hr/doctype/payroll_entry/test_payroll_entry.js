QUnit.module('HR');

QUnit.test("test: Payroll Entry", function (assert) {
	assert.expect(5);
	let done = assert.async();
	let employees, docname;

	dataent.run_serially([
		() => {
			return dataent.tests.make('Payroll Entry', [
				{company: 'For Testing'},
				{posting_date: dataent.datetime.add_days(dataent.datetime.nowdate(), 0)},
				{payroll_frequency: 'Monthly'},
				{cost_center: 'Main - '+dataent.get_abbr(dataent.defaults.get_default("Company"))}
			]);
		},

		() => dataent.timeout(1),
		() => {
			assert.equal(cur_frm.doc.company, 'For Testing');
			assert.equal(cur_frm.doc.posting_date, dataent.datetime.add_days(dataent.datetime.nowdate(), 0));
			assert.equal(cur_frm.doc.cost_center, 'Main - FT');
		},
		() => dataent.click_button('Get Employee Details'),
		() => {
			employees = cur_frm.doc.employees.length;
			docname = cur_frm.doc.name;
		},

		() => dataent.click_button('Submit'),
		() => dataent.timeout(1),
		() => dataent.click_button('Yes'),
		() => dataent.timeout(5),

		() => dataent.click_button('View Salary Slip'),
		() => dataent.timeout(2),
		() => assert.equal(cur_list.data.length, employees),

		() => dataent.set_route('Form', 'Payroll Entry', docname),
		() => dataent.timeout(2),
		() => dataent.click_button('Submit Salary Slip'),
		() => dataent.click_button('Yes'),
		() => dataent.timeout(5),

		() => dataent.click_button('Close'),
		() => dataent.timeout(1),

		() => dataent.click_button('View Salary Slip'),
		() => dataent.timeout(2),
		() => {
			let count = 0;
			for(var i = 0; i < employees; i++) {
				if(cur_list.data[i].docstatus == 1){
					count++;
				}
			}
			assert.equal(count, employees, "Salary Slip submitted for all employees");
		},

		() => done()
	]);
});
