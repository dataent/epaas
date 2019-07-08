QUnit.module('Stock');

QUnit.test("test Purchase Receipt", function(assert) {
	assert.expect(4);
	let done = assert.async();
	dataent.run_serially([
		() => {
			return dataent.tests.make('Purchase Receipt', [
				{supplier: 'Test Supplier'},
				{items: [
					[
						{'received_qty': 5},
						{'qty': 4},
						{'item_code': 'Test Product 1'},
						{'uom': 'Nos'},
						{'warehouse':'Stores - '+dataent.get_abbr(dataent.defaults.get_default('Company'))},
						{'rejected_warehouse':'Work In Progress - '+dataent.get_abbr(dataent.defaults.get_default('Company'))},
					]
				]},
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
			// get tax account head details
			assert.ok(cur_frm.doc.taxes[0].account_head=='CGST - '+dataent.get_abbr(dataent.defaults.get_default('Company')), " Account Head abbr correct");
			// grand_total Calculated
			assert.ok(cur_frm.doc.grand_total==472, "Grad Total correct");

		},
		() => dataent.tests.click_button('Submit'),
		() => dataent.tests.click_button('Yes'),
		() => dataent.timeout(0.3),
		() => done()
	]);
});
