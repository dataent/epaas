dataent.provide('epaas.hub');

dataent.views.MarketplaceFactory = class MarketplaceFactory extends dataent.views.Factory {
	show() {
		is_marketplace_disabled()
			.then(disabled => {
				if (disabled) {
					dataent.show_not_found('Marketplace');
					return;
				}

				if (dataent.pages.marketplace) {
					dataent.container.change_to('marketplace');
					epaas.hub.marketplace.refresh();
				} else {
					this.make('marketplace');
				}
			});
	}

	make(page_name) {
		const assets = [
			'/assets/js/marketplace.min.js'
		];

		dataent.require(assets, () => {
			epaas.hub.marketplace = new epaas.hub.Marketplace({
				parent: this.make_page(true, page_name)
			});
		});
	}
};

function is_marketplace_disabled() {
	return dataent.call({
		method: "epaas.hub_node.doctype.marketplace_settings.marketplace_settings.is_marketplace_enabled"
	}).then(r => r.message)
}

$(document).on('toolbar_setup', () => {
	$('#toolbar-user .navbar-reload').after(`
		<li>
			<a class="marketplace-link" href="#marketplace/home">${__('Marketplace')}
		</li>
	`);

	is_marketplace_disabled()
		.then(disabled => {
			if (disabled) {
				$('#toolbar-user .marketplace-link').hide();
			}
		});
});
