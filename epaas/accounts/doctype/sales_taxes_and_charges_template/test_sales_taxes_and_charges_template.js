QUnit.module('Sales Taxes and Charges Template');

QUnit.test("test sales taxes and charges template", function(assert) {
	assert.expect(2);
	let done = assert.async();
	dataent.run_serially([
		() => {
			return dataent.tests.make('Sales Taxes and Charges Template', [
				{title: "TEST In State GST"},
				{taxes:[
					[
						{charge_type:"On Net Total"},
						{account_head:"CGST - "+dataent.get_abbr(dataent.defaults.get_default("Company")) }
					],
					[
						{charge_type:"On Net Total"},
						{account_head:"SGST - "+dataent.get_abbr(dataent.defaults.get_default("Company")) }
					]
				]}
			]);
		},
		() => {
			assert.ok(cur_frm.doc.title=='TEST In State GST');
			assert.ok(cur_frm.doc.name=='TEST In State GST - FT');
		},
		() => done()
	]);
});

