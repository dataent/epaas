QUnit.module("sales");

QUnit.test("test: lead", function (assert) {
	assert.expect(5);
	let done = assert.async();
	let lead_name = dataent.utils.get_random(10);
	dataent.run_serially([
		// test lead creation
		() => dataent.set_route("List", "Lead"),
		() => dataent.new_doc("Lead"),
		() => dataent.timeout(1),
		() => cur_frm.set_value("organization_lead", "1"),
		() => cur_frm.set_value("company_name", lead_name),
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

		() => dataent.click_button('New Contact'),
		() => dataent.timeout(1),
		() => dataent.set_control('first_name', 'John'),
		() => dataent.set_control('last_name', 'Doe'),
		() => cur_frm.save(),
		() => dataent.timeout(3),
		() => dataent.set_route('Form', 'Lead', cur_frm.doc.links[0].link_name),
		() => dataent.timeout(1),
		() => dataent.click_link('Address & Contact'),
		() => assert.ok($('.address-box').text().includes('John'),
			'contact is seen in contact box'),

		// make customer
		() => dataent.click_button('Make'),
		() => dataent.click_link('Customer'),
		() => dataent.timeout(2),
		() => assert.equal(cur_frm.doc.lead_name, dataent.lead_name,
			'lead name correctly mapped'),

		() => done()
	]);
});
