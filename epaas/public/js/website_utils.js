// Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

if(!window.epaas) window.epaas = {};

// Add / update a new Lead / Communication
// subject, sender, description
dataent.send_message = function(opts, btn) {
	return dataent.call({
		type: "POST",
		method: "epaas.templates.utils.send_message",
		btn: btn,
		args: opts,
		callback: opts.callback
	});
};

epaas.subscribe_to_newsletter = function(opts, btn) {
	return dataent.call({
		type: "POST",
		method: "dataent.email.doctype.newsletter.newsletter.subscribe",
		btn: btn,
		args: {"email": opts.email},
		callback: opts.callback
	});
}

// for backward compatibility
epaas.send_message = dataent.send_message;
