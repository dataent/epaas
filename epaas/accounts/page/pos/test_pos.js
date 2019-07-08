QUnit.test("test:Sales Invoice", function(assert) {
	assert.expect(3);
	let done = assert.async();

	dataent.run_serially([
		() => {
			return dataent.tests.make("POS Profile", [
				{naming_series: "SINV"},
				{pos_profile_name: "_Test POS Profile"},
				{country: "India"},
				{currency: "INR"},
				{write_off_account: "Write Off - FT"},
				{write_off_cost_center: "Main - FT"},
				{payments: [
					[
						{"default": 1},
						{"mode_of_payment": "Cash"}
					]]
				}
			]);
		},
		() => cur_frm.save(),
		() => dataent.timeout(2),
		() => {
			assert.equal(cur_frm.doc.payments[0].default, 1, "Default mode of payment tested");
		},
		() => dataent.timeout(1),
		() => {
			return dataent.tests.make("Sales Invoice", [
				{customer: "Test Customer 2"},
				{is_pos: 1},
				{posting_date: dataent.datetime.get_today()},
				{due_date: dataent.datetime.get_today()},
				{items: [
					[
						{"item_code": "Test Product 1"},
						{"qty": 5},
						{"warehouse":'Stores - FT'}
					]]
				}
			]);
		},
		() => dataent.timeout(2),
		() => cur_frm.save(),
		() => dataent.timeout(2),
		() => {
			assert.equal(cur_frm.doc.payments[0].default, 1, "Default mode of payment tested");
			assert.equal(cur_frm.doc.payments[0].mode_of_payment, "Cash", "Default mode of payment tested");
		},
		() => done()
	]);
});