QUnit.module('Quotation');

QUnit.test("test quotation with taxes and charges", function(assert) {
	assert.expect(3);
	let done = assert.async();
	dataent.run_serially([
		() => {
			return dataent.tests.make('Quotation', [
				{customer: 'Test Customer 1'},
				{items: [
					[
						{'delivery_date': dataent.datetime.add_days(dataent.defaults.get_default("year_end_date"), 1)},
						{'qty': 5},
						{'item_code': 'Test Product 4'},
					]
				]},
				{customer_address: 'Test1-Billing'},
				{shipping_address_name: 'Test1-Shipping'},
				{contact_person: 'Contact 1-Test Customer 1'},
				{taxes_and_charges: 'TEST In State GST - FT'},
				{tc_name: 'Test Term 1'},
				{terms: 'This is Test'}
			]);
		},
		() => cur_frm.save(),
		() => {
			// get_item_details
			assert.ok(cur_frm.doc.items[0].item_name=='Test Product 4', "Item name correct");
			// get tax details
			assert.ok(cur_frm.doc.taxes_and_charges=='TEST In State GST - FT', "Tax details correct");
			// get tax account head details
			assert.ok(cur_frm.doc.taxes[0].account_head=='CGST - '+dataent.get_abbr(dataent.defaults.get_default('Company')), " Account Head abbr correct");

		},
		() => dataent.tests.click_button('Submit'),
		() => dataent.tests.click_button('Yes'),
		() => dataent.timeout(0.3),
		() => done()
	]);
});

