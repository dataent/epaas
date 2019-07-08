dataent.listview_settings['Employee'] = {
	add_fields: ["status", "branch", "department", "designation","image"],
	filters: [["status","=", "Active"]],
	get_indicator: function(doc) {
		var indicator = [__(doc.status), dataent.utils.guess_colour(doc.status), "status,=," + doc.status];
		indicator[1] = {"Active": "green", "Temporary Leave": "red", "Left": "darkgrey"}[doc.status];
		return indicator;
	}
};