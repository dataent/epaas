QUnit.module("sales");

QUnit.test("test: lead", function (assert) {
	assert.expect(4);
	let done = assert.async();
	let lead_name = dataent.utils.get_random(10);
	dataent.run_serially([
		// test lead creation
		() => dataent.set_route("List", "Lead"),
		() => dataent.new_doc("Lead"),
		() => dataent.timeout(1),
		() => cur_frm.set_value("lead_name", lead_name),
		() => cur_frm.save(),
		() => dataent.timeout(1),
		() => {
			assert.ok(cur_frm.doc.lead_name.includes(lead_name),
				'name correctly set');
			dataent.lead_name = cur_frm.doc.name;
		},
		// create address and contact
		() => dataent.click_link('Address & Contact'),
		() => dataent.click_button('New Address'),
		() => dataent.timeout(1),
		() => dataent.set_control('address_line1', 'Gateway'),
		() => dataent.set_control('city', 'Mumbai'),
		() => cur_frm.save(),
		() => dataent.timeout(3),
		() => assert.equal(dataent.get_route()[1], 'Lead',
			'back to lead form'),
		() => dataent.click_link('Address & Contact'),
		() => assert.ok($('.address-box').text().includes('Mumbai'),
			'city is seen in address box'),

		// make opportunity
		() => dataent.click_button('Make'),
		() => dataent.click_link('Opportunity'),
		() => dataent.timeout(2),
		() => assert.equal(cur_frm.doc.lead, dataent.lead_name,
			'lead name correctly mapped'),

		() => done()
	]);
});
