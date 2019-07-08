// Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

dataent.provide('epaas');

// add toolbar icon
$(document).bind('toolbar_setup', function() {
	dataent.app.name = "EPAAS";

	dataent.help_feedback_link = '<p><a class="text-muted" \
		href="https://discuss.epaas.xyz">Feedback</a></p>'


	$('.navbar-home').html('<img class="epaas-icon" src="'+
			dataent.urllib.get_base_url()+'/assets/epaas/images/erp-icon.svg" />');

	$('[data-link="docs"]').attr("href", "https://epaas.xyz/docs")
	$('[data-link="issues"]').attr("href", "https://github.com/dataent/epaas/issues")


	// default documentation goes to epaas
	// $('[data-link-type="documentation"]').attr('data-path', '/epaas/manual/index');

	// additional help links for epaas
	var $help_menu = $('.dropdown-help ul .documentation-links');
	$('<li><a data-link-type="forum" href="https://epaas.xyz/docs/user/manual" \
		target="_blank">'+__('Documentation')+'</a></li>').insertBefore($help_menu);
	$('<li><a data-link-type="forum" href="https://discuss.epaas.xyz" \
		target="_blank">'+__('User Forum')+'</a></li>').insertBefore($help_menu);
	$('<li><a href="https://github.com/dataent/epaas/issues" \
		target="_blank">'+__('Report an Issue')+'</a></li>').insertBefore($help_menu);

});



// doctypes created via tree
$.extend(dataent.create_routes, {
	"Customer Group": "Tree/Customer Group",
	"Territory": "Tree/Territory",
	"Item Group": "Tree/Item Group",
	"Sales Person": "Tree/Sales Person",
	"Account": "Tree/Account",
	"Cost Center": "Tree/Cost Center",
	"Department": "Tree/Department",
});

// preferred modules for breadcrumbs
$.extend(dataent.breadcrumbs.preferred, {
	"Item Group": "Stock",
	"Customer Group": "Selling",
	"Supplier Group": "Buying",
	"Territory": "Selling",
	"Sales Person": "Selling",
	"Sales Partner": "Selling",
	"Brand": "Selling"
});
