QUnit.module('accounts');

QUnit.test("test account with number", function(assert) {
	assert.expect(7);
	let done = assert.async();
	dataent.run_serially([
		() => dataent.set_route('Tree', 'Account'),
		() => dataent.click_link('Income'),
		() => dataent.click_button('Add Child'),
		() => dataent.timeout(.5),
		() => {
			cur_dialog.fields_dict.account_name.$input.val("Test Income");
			cur_dialog.fields_dict.account_number.$input.val("4010");
		},
		() => dataent.click_button('Create New'),
		() => dataent.timeout(1),
		() => {
			assert.ok($('a:contains("4010 - Test Income"):visible').length!=0, "Account created with number");
		},
		() => dataent.click_link('4010 - Test Income'),
		() => dataent.click_button('Edit'),
		() => dataent.timeout(.5),
		() => dataent.click_button('Update Account Number'),
		() => dataent.timeout(.5),
		() => {
			cur_dialog.fields_dict.account_number.$input.val("4020");
		},
		() => dataent.timeout(1),
		() => cur_dialog.primary_action(),
		() => dataent.timeout(1),
		() => cur_frm.refresh_fields(),
		() => dataent.timeout(.5),
		() => {
			var abbr = dataent.get_abbr(dataent.defaults.get_default("Company"));
			var new_account = "4020 - Test Income - " + abbr;
			assert.ok(cur_frm.doc.name==new_account, "Account renamed");
			assert.ok(cur_frm.doc.account_name=="Test Income", "account name remained same");
			assert.ok(cur_frm.doc.account_number=="4020", "Account number updated to 4020");
		},
		() => dataent.timeout(1),
		() => dataent.click_button('Menu'),
		() => dataent.click_link('Rename'),
		() => dataent.timeout(.5),
		() => {
			cur_dialog.fields_dict.new_name.$input.val("4030 - Test Income");
		},
		() => dataent.timeout(.5),
		() => dataent.click_button("Rename"),
		() => dataent.timeout(2),
		() => {
			assert.ok(cur_frm.doc.account_name=="Test Income", "account name remained same");
			assert.ok(cur_frm.doc.account_number=="4030", "Account number updated to 4030");
		},
		() => dataent.timeout(.5),
		() => dataent.click_button('Chart of Accounts'),
		() => dataent.timeout(.5),
		() => dataent.click_button('Menu'),
		() => dataent.click_link('Refresh'),
		() => dataent.click_button('Expand All'),
		() => dataent.click_link('4030 - Test Income'),
		() => dataent.click_button('Delete'),
		() => dataent.click_button('Yes'),
		() => dataent.timeout(.5),
		() => {
			assert.ok($('a:contains("4030 - Test Account"):visible').length==0, "Account deleted");
		},
		() => done()
	]);
});
