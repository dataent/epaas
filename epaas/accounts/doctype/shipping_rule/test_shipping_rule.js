QUnit.module('Shipping Rule');

QUnit.test("test Shipping Rule", function(assert) {
	assert.expect(1);
	let done = assert.async();
	dataent.run_serially([
		() => {
			return dataent.tests.make("Shipping Rule", [
				{label: "Next Day Shipping"},
				{shipping_rule_type: "Selling"},
				{calculate_based_on: 'Net Total'},
				{conditions:[
					[
						{from_value:1},
						{to_value:200},
						{shipping_amount:100}
					],
					[
						{from_value:201},
						{to_value:2000},
						{shipping_amount:50}
					],
				]},
				{countries:[
					[
						{country:'India'}
					]
				]},
				{account:'Accounts Payable - '+dataent.get_abbr(dataent.defaults.get_default("Company"))},
				{cost_center:'Main - '+dataent.get_abbr(dataent.defaults.get_default("Company"))}
			]);
		},
		() => {assert.ok(cur_frm.doc.name=='Next Day Shipping');},
		() => done()
	]);
});

