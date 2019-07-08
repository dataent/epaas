QUnit.test("test salary slip", function(assert) {
	assert.expect(6);
	let done = assert.async();
	let employee_name;

	let salary_slip = (ename) => {
		dataent.run_serially([
			() => dataent.db.get_value('Employee', {'employee_name': ename}, 'name'),
			(r) => {
				employee_name = r.message.name;
			},
			() => {
				// Creating a salary slip for a employee
				dataent.tests.make('Salary Slip', [
					{ employee: employee_name}
				]);
			},
			() => dataent.timeout(3),
			() => {
			// To check if all the calculations are correctly done
				if(ename === 'Test Employee 1')
				{
					assert.ok(cur_frm.doc.gross_pay==24000,
						'Gross amount for first employee is correctly calculated');
					assert.ok(cur_frm.doc.total_deduction==4800,
						'Deduction amount for first employee is correctly calculated');
					assert.ok(cur_frm.doc.net_pay==19200,
						'Net amount for first employee is correctly calculated');
				}
				if(ename === 'Test Employee 3')
				{
					assert.ok(cur_frm.doc.gross_pay==28800,
						'Gross amount for second employee is correctly calculated');
					assert.ok(cur_frm.doc.total_deduction==5760,
						'Deduction amount for second employee is correctly calculated');
					assert.ok(cur_frm.doc.net_pay==23040,
						'Net amount for second employee is correctly calculated');
				}
			},
		]);
	};
	dataent.run_serially([
		() => salary_slip('Test Employee 1'),
		() => dataent.timeout(6),
		() => salary_slip('Test Employee 3'),
		() => dataent.timeout(5),
		() => dataent.set_route('List', 'Salary Slip', 'List'),
		() => dataent.timeout(2),
		() => {$('.list-row-checkbox').click();},
		() => dataent.timeout(2),
		() => dataent.click_button('Delete'),
		() => dataent.click_button('Yes'),
		() => done()
	]);
});