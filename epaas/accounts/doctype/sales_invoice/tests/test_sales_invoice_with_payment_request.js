QUnit.module('Sales Invoice');

QUnit.test("test sales Invoice with payment request", function(assert) {
	assert.expect(4);
	let done = assert.async();
	dataent.run_serially([
		() => {
			return dataent.tests.make('Sales Invoice', [
				{customer: 'Test Customer 1'},
				{items: [
					[
						{'qty': 5},
						{'item_code': 'Test Product 1'},
					]
				]},
				{update_stock:1},
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
			assert.ok(cur_frm.doc.items[0].item_name=='Test Product 1', "Item name correct");
			// get tax details
			assert.ok(cur_frm.doc.taxes_and_charges=='TEST In State GST - FT', "Tax details correct");
			// grand_total Calculated
			assert.ok(cur_frm.doc.grand_total==590, "Grad Total correct");

		},
		() => dataent.tests.click_button('Submit'),
		() => dataent.tests.click_button('Yes'),
		() => dataent.timeout(2),
		() => dataent.tests.click_button('Close'),
		() => dataent.tests.click_button('Make'),
		() => dataent.tests.click_link('Payment Request'),
		() => dataent.timeout(0.2),
		() => { cur_frm.set_value('print_format','GST Tax Invoice');},
		() => { cur_frm.set_value('email_to','test@gmail.com');},
		() => cur_frm.save(),
		() => {
			// get payment details
			assert.ok(cur_frm.doc.grand_total==590, "grand total Correct");
		},
		() => done()
	]);
});

