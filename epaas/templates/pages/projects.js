dataent.ready(function() {

	$('.task-status-switch').on('click', function() {
		var $btn = $(this);
		if($btn.attr('data-status')==='Open') {
			reload_items('closed', 'task', $btn);
		} else {
			reload_items('open', 'task', $btn);
		}
	})


	$('.issue-status-switch').on('click', function() {
		var $btn = $(this);
		if($btn.attr('data-status')==='Open') {
			reload_items('closed', 'issue', $btn);
		} else {
			reload_items('open', 'issue', $btn);
		}
	})

	var start = 10;
	$(".more-tasks").click(function() {
		more_items('task', true);
	});

	$(".more-issues").click(function() {
		more_items('issue', true);
	});

	$(".more-timelogs").click(function() {
		more_items('timelog', false);
	});

	$(".more-timelines").click(function() {
		more_items('timeline', false);
	});

	$(".file-size").each(function() {
		$(this).text(dataent.form.formatters.FileSize($(this).text()));
	});


	var reload_items = function(item_status, item, $btn) {
		$.ajax({
			method: "GET",
			url: "/",
			dataType: "json",
			data: {
				cmd: "epaas.templates.pages.projects.get_"+ item +"_html",
				project: '{{ doc.name }}',
				item_status: item_status,
			},
			success: function(data) {
				if(typeof data.message == 'undefined') {
					$('.project-'+ item).html("No "+ item_status +" "+ item);
					$(".more-"+ item).toggle(false);
				}
				$('.project-'+ item).html(data.message);
				$(".more-"+ item).toggle(true);

				// update status
				if(item_status==='open') {
					$btn.html(__('Show closed')).attr('data-status', 'Open');
				} else {
					$btn.html(__('Show open')).attr('data-status', 'Closed');
				}
			}
		});

	}

	var more_items = function(item, item_status){
		if(item_status) {
			var item_status = $('.project-'+ item +'-section .btn-group .bold').hasClass('btn-closed-'+ item)
				? 'closed' : 'open';
		}
		$.ajax({
			method: "GET",
			url: "/",
			dataType: "json",
			data: {
				cmd: "epaas.templates.pages.projects.get_"+ item +"_html",
				project: '{{ doc.name }}',
				start: start,
				item_status: item_status,
			},
			success: function(data) {

				$(data.message).appendTo('.project-'+ item);
				if(typeof data.message == 'undefined') {
					$(".more-"+ item).toggle(false);
				}
				start = start+10;
			}
		});
	}

	var close_item = function(item, item_name){
		var args = {
			project: '{{ doc.name }}',
			item_name: item_name,
		}
		dataent.call({
			btn: this,
			type: "POST",
			method: "epaas.templates.pages.projects.set_"+ item +"_status",
			args: args,
			callback: function(r) {
				if(r.exc) {
					if(r._server_messages)
						dataent.msgprint(r._server_messages);
				} else {
					$(this).remove();
				}
			}
		})
		return false;
	}
});