QUnit.module('Journal Entry');

QUnit.test("test journal entry", function(assert) {
	assert.expect(2);
	let done = assert.async();
	dataent.run_serially([
		() => {
			return dataent.tests.make('Journal Entry', [
				{posting_date:dataent.datetime.add_days(dataent.datetime.nowdate(), 0)},
				{accounts: [
					[
						{'account':'Debtors - '+dataent.get_abbr(dataent.defaults.get_default('Company'))},
						{'party_type':'Customer'},
						{'party':'Test Customer 1'},
						{'credit_in_account_currency':1000},
						{'is_advance':'Yes'},
					],
					[
						{'account':'HDFC - '+dataent.get_abbr(dataent.defaults.get_default('Company'))},
						{'debit_in_account_currency':1000},
					]
				]},
				{cheque_no:1234},
				{cheque_date: dataent.datetime.add_days(dataent.datetime.nowdate(), -1)},
				{user_remark: 'Test'},
			]);
		},
		() => cur_frm.save(),
		() => {
			// get_item_details
			assert.ok(cur_frm.doc.total_debit==1000, "total debit correct");
			assert.ok(cur_frm.doc.total_credit==1000, "total credit correct");
		},
		() => dataent.tests.click_button('Submit'),
		() => dataent.tests.click_button('Yes'),
		() => dataent.timeout(0.3),
		() => done()
	]);
});
