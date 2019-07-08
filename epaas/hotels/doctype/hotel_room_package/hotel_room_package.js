// Copyright (c) 2017, Dataent Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

dataent.ui.form.on('Hotel Room Package', {
	hotel_room_type: function(frm) {
		if (frm.doc.hotel_room_type) {
			dataent.model.with_doc('Hotel Room Type', frm.doc.hotel_room_type, () => {
				let hotel_room_type = dataent.get_doc('Hotel Room Type', frm.doc.hotel_room_type);

				// reset the amenities
				frm.doc.amenities = [];

				for (let amenity of hotel_room_type.amenities) {
					let d = frm.add_child('amenities');
					d.item = amenity.item;
					d.billable = amenity.billable;
				}

				frm.refresh();
			});
		}
	}
});
