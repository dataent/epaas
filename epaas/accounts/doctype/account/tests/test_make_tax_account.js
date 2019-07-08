QUnit.module('accounts');
QUnit.test("test account", assert => {
	assert.expect(3);
	let done = assert.async();
	dataent.run_serially([
		() => dataent.set_route('Tree', 'Account'),
		() => dataent.click_button('Expand All'),
		() => dataent.click_link('Duties and Taxes - '+ dataent.get_abbr(dataent.defaults.get_default("Company"))),
		() => {
			if($('a:contains("CGST"):visible').length == 0){
				return dataent.map_tax.make('CGST', 9);
			}
		},
		() => {
			if($('a:contains("SGST"):visible').length == 0){
				return dataent.map_tax.make('SGST', 9);
			}
		},
		() => {
			if($('a:contains("IGST"):visible').length == 0){
				return dataent.map_tax.make('IGST', 18);
			}
		},
		() => {
			assert.ok($('a:contains("CGST"):visible').length!=0, "CGST Checked");
			assert.ok($('a:contains("SGST"):visible').length!=0, "SGST Checked");
			assert.ok($('a:contains("IGST"):visible').length!=0, "IGST Checked");
		},
		() => done()
	]);
});


dataent.map_tax = {
	make:function(text,rate){
		return dataent.run_serially([
			() => dataent.click_button('Add Child'),
			() => dataent.timeout(0.2),
			() => cur_dialog.set_value('account_name',text),
			() => cur_dialog.set_value('account_type','Tax'),
			() => cur_dialog.set_value('tax_rate',rate),
			() => cur_dialog.set_value('account_currency','INR'),
			() => dataent.click_button('Create New'),
		]);
	}
};
