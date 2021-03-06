QUnit.module('HR');

QUnit.test("test: Set Salary Components", function (assert) {
	assert.expect(5);
	let done = assert.async();

	dataent.run_serially([
		() => dataent.set_route('Form', 'Salary Component', 'Leave Encashment'),
		() => {
			var row = dataent.model.add_child(cur_frm.doc, "Salary Component Account", "accounts");
			row.company = 'For Testing';
			row.default_account = 'Salary - FT';
		},

		() => cur_frm.save(),
		() => dataent.timeout(2),
		() => assert.equal(cur_frm.doc.accounts[0].default_account, 'Salary - FT'),

		() => dataent.set_route('Form', 'Salary Component', 'Basic'),
		() => {
			var row = dataent.model.add_child(cur_frm.doc, "Salary Component Account", "accounts");
			row.company = 'For Testing';
			row.default_account = 'Salary - FT';
		},

		() => cur_frm.save(),
		() => dataent.timeout(2),
		() => assert.equal(cur_frm.doc.accounts[0].default_account, 'Salary - FT'),

		() => dataent.set_route('Form', 'Salary Component', 'Income Tax'),
		() => {
			var row = dataent.model.add_child(cur_frm.doc, "Salary Component Account", "accounts");
			row.company = 'For Testing';
			row.default_account = 'Salary - FT';
		},

		() => cur_frm.save(),
		() => dataent.timeout(2),
		() => assert.equal(cur_frm.doc.accounts[0].default_account, 'Salary - FT'),

		() => dataent.set_route('Form', 'Salary Component', 'Arrear'),
		() => {
			var row = dataent.model.add_child(cur_frm.doc, "Salary Component Account", "accounts");
			row.company = 'For Testing';
			row.default_account = 'Salary - FT';
		},

		() => cur_frm.save(),
		() => dataent.timeout(2),
		() => assert.equal(cur_frm.doc.accounts[0].default_account, 'Salary - FT'),

		() => dataent.set_route('Form', 'Company', 'For Testing'),
		() => cur_frm.set_value('default_payroll_payable_account', 'Payroll Payable - FT'),
		() => cur_frm.save(),
		() => dataent.timeout(2),
		() => assert.equal(cur_frm.doc.default_payroll_payable_account, 'Payroll Payable - FT'),

		() => done()

	]);
});
