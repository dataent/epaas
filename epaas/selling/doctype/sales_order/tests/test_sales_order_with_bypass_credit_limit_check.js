QUnit.module('Sales Order');

QUnit.test("test_sales_order_with_bypass_credit_limit_check", function(assert) {
//#PR : 10861, Author : ashish-greycube & jigneshpshah,  Email:mr.ashish.shah@gmail.com 
	assert.expect(2);
	let done = assert.async();
	dataent.run_serially([
		() => dataent.new_doc('Customer'),
		() => dataent.timeout(1),
		() => dataent.quick_entry.dialog.$wrapper.find('.edit-full').click(),
		() => dataent.timeout(1),
		() => cur_frm.set_value("customer_name", "Test Customer 10"),
		() => cur_frm.set_value("credit_limit", 100.00),
		() => cur_frm.set_value("bypass_credit_limit_check_at_sales_order", 1),
		// save form
		() => cur_frm.save(),
		() => dataent.timeout(1),

		() => dataent.new_doc('Item'),
		() => dataent.timeout(1),
		() => dataent.quick_entry.dialog.$wrapper.find('.edit-full').click(),
		() => dataent.timeout(1),
		() => cur_frm.set_value("item_code", "Test Product 10"),
		() => cur_frm.set_value("item_group", "Products"),
		() => cur_frm.set_value("standard_rate", 100),	
		// save form
		() => cur_frm.save(),
		() => dataent.timeout(1),		

		() => {
			return dataent.tests.make('Sales Order', [
				{customer: 'Test Customer 5'},
				{items: [
					[
						{'delivery_date': dataent.datetime.add_days(dataent.defaults.get_default("year_end_date"), 1)},
						{'qty': 5},
						{'item_code': 'Test Product 10'},
					]
				]}

			]);
		},
		() => cur_frm.save(),
		() => dataent.tests.click_button('Submit'),
		() => assert.equal("Confirm", cur_dialog.title,'confirmation for submit'),
		() => dataent.tests.click_button('Yes'),
		() => dataent.timeout(3),
		() => {
			
			assert.ok(cur_frm.doc.status=="To Deliver and Bill", "It is submited. Credit limit is NOT checked for sales order");


		},		
		() => done()
	]);
});
