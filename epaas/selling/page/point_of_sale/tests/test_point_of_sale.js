QUnit.test("test:Point of Sales", function(assert) {
	assert.expect(1);
	let done = assert.async();

	dataent.run_serially([
		() => dataent.set_route('point-of-sale'),
		() => dataent.timeout(3),
		() => dataent.set_control('customer', 'Test Customer 1'),
		() => dataent.timeout(0.2),
		() => cur_frm.set_value('customer', 'Test Customer 1'),
		() => dataent.timeout(2),
		() => dataent.click_link('Test Product 2'),
		() => dataent.timeout(0.2),
		() => dataent.click_element(`.cart-items [data-item-code="Test Product 2"]`),
		() => dataent.timeout(0.2),
		() => dataent.click_element(`.number-pad [data-value="Rate"]`),
		() => dataent.timeout(0.2),
		() => dataent.click_element(`.number-pad [data-value="2"]`),
		() => dataent.timeout(0.2),
		() => dataent.click_element(`.number-pad [data-value="5"]`),
		() => dataent.timeout(0.2),
		() => dataent.click_element(`.number-pad [data-value="0"]`),
		() => dataent.timeout(0.2),
		() => dataent.click_element(`.number-pad [data-value="Pay"]`),
		() => dataent.timeout(0.2),
		() => dataent.click_element(`.dataent-control [data-value="4"]`),
		() => dataent.timeout(0.2),
		() => dataent.click_element(`.dataent-control [data-value="5"]`),
		() => dataent.timeout(0.2),
		() => dataent.click_element(`.dataent-control [data-value="0"]`),
		() => dataent.timeout(0.2),
		() => dataent.click_button('Submit'),
		() => dataent.click_button('Yes'),
		() => dataent.timeout(3),
		() => assert.ok(cur_frm.doc.docstatus==1, "Sales invoice created successfully"),
		() => done()
	]);
});