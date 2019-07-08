QUnit.module('Buying');

QUnit.test("test: request_for_quotation", function(assert) {
	assert.expect(14);
	let done = assert.async();
	let date;
	dataent.run_serially([
		() => {
			date = dataent.datetime.add_days(dataent.datetime.now_date(), 10);
			return dataent.tests.make('Request for Quotation', [
				{transaction_date: date},
				{suppliers: [
					[
						{"supplier": 'Test Supplier'},
						{"email_id": 'test@supplier.com'}
					]
				]},
				{items: [
					[
						{"item_code": 'Test Product 4'},
						{"qty": 5},
						{"schedule_date": dataent.datetime.add_days(dataent.datetime.now_date(),20)},
						{"warehouse": 'All Warehouses - '+dataent.get_abbr(dataent.defaults.get_default("Company"))}
					]
				]},
				{message_for_supplier: 'Please supply the specified items at the best possible rates'},
				{tc_name: 'Test Term 1'}
			]);
		},
		() => dataent.timeout(3),
		() => {
			assert.ok(cur_frm.doc.transaction_date == date, "Date correct");
			assert.ok(cur_frm.doc.company == cur_frm.doc.company, "Company correct");
			assert.ok(cur_frm.doc.suppliers[0].supplier_name == 'Test Supplier', "Supplier name correct");
			assert.ok(cur_frm.doc.suppliers[0].contact == 'Contact 3-Test Supplier', "Contact correct");
			assert.ok(cur_frm.doc.suppliers[0].email_id == 'test@supplier.com', "Email id correct");
			assert.ok(cur_frm.doc.items[0].item_name == 'Test Product 4', "Item Name correct");
			assert.ok(cur_frm.doc.items[0].warehouse == 'All Warehouses - '+dataent.get_abbr(dataent.defaults.get_default("Company")), "Warehouse correct");
			assert.ok(cur_frm.doc.message_for_supplier == 'Please supply the specified items at the best possible rates', "Reply correct");
			assert.ok(cur_frm.doc.tc_name == 'Test Term 1', "Term name correct");
		},
		() => dataent.timeout(3),
		() => cur_frm.print_doc(),
		() => dataent.timeout(1),
		() => {
			assert.ok($('.btn-print-print').is(':visible'), "Print Format Available");
			assert.ok($('.section-break+ .section-break .column-break:nth-child(1) .value').text().includes("Test Product 4"), "Print Preview Works");
		},
		() => cur_frm.print_doc(),
		() => dataent.timeout(1),
		() => dataent.click_button('Get items from'),
		() => dataent.timeout(0.3),
		() => dataent.click_link('Material Request'),
		() => dataent.timeout(1),
		() => dataent.click_button('Get Items'),
		() => dataent.timeout(1),
		() => {
			assert.ok(cur_frm.doc.items[1].item_name == 'Test Product 1', "Getting items from material requests work");
		},
		() => cur_frm.save(),
		() => dataent.timeout(1),
		() => dataent.tests.click_button('Submit'),
		() => dataent.tests.click_button('Yes'),
		() => dataent.timeout(1),
		() => {
			assert.ok(cur_frm.doc.docstatus == 1, "Quotation request submitted");
		},
		() => dataent.click_button('Send Supplier Emails'),
		() => dataent.timeout(6),
		() => {
			assert.ok($('div.modal.fade.in > div.modal-dialog > div > div.modal-body.ui-front > div.msgprint').text().includes("Email sent to supplier Test Supplier"), "Send emails working");
		},
		() => dataent.click_button('Close'),
		() => done()
	]);
});