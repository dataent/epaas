dataent.pages['team-updates'].on_page_load = function(wrapper) {
	var page = dataent.ui.make_app_page({
		parent: wrapper,
		title: __('Team Updates'),
		single_column: true
	});

	dataent.team_updates.make(page);
	dataent.team_updates.run();

	if(dataent.model.can_read('Daily Work Summary Group')) {
		page.add_menu_item(__('Daily Work Summary Group'), function() {
			dataent.set_route('Form', 'Daily Work Summary Group');
		});
	}
}

dataent.team_updates = {
	start: 0,
	make: function(page) {
		var me = dataent.team_updates;
		me.page = page;
		me.body = $('<div></div>').appendTo(me.page.main);
		me.more = $('<div class="for-more"><button class="btn btn-sm btn-default btn-more">'
			+ __("More") + '</button></div>').appendTo(me.page.main)
			.find('.btn-more').on('click', function() {
				me.start += 40;
				me.run();
			});
	},
	run: function() {
		var me = dataent.team_updates;
		dataent.call({
			method: 'epaas.hr.page.team_updates.team_updates.get_data',
			args: {
				start: me.start
			},
			callback: function(r) {
				if(r.message) {
					r.message.forEach(function(d) {
						me.add_row(d);
					});
				} else {
					dataent.show_alert({message:__('No more updates'), indicator:'darkgrey'});
					me.more.parent().addClass('hidden');
				}
			}
		});
	},
	add_row: function(data) {
		var me = dataent.team_updates;

		data.by = dataent.user.full_name(data.sender);
		data.avatar = dataent.avatar(data.sender);
		data.when = comment_when(data.creation);

		var date = dataent.datetime.str_to_obj(data.creation);
		var last = me.last_feed_date;

		if((last && dataent.datetime.obj_to_str(last) != dataent.datetime.obj_to_str(date)) || (!last)) {
			var diff = dataent.datetime.get_day_diff(dataent.datetime.get_today(), dataent.datetime.obj_to_str(date));
			var pdate;
			if(diff < 1) {
				pdate = 'Today';
			} else if(diff < 2) {
				pdate = 'Yesterday';
			} else {
				pdate = dataent.datetime.global_date_format(date);
			}
			data.date_sep = pdate;
			data.date_class = pdate=='Today' ? "date-indicator blue" : "date-indicator";
		} else {
			data.date_sep = null;
			data.date_class = "";
		}
		me.last_feed_date = date;

		$(dataent.render_template('team_update_row', data)).appendTo(me.body)
	}
}