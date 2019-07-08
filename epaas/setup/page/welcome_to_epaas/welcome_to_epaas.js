dataent.pages['welcome-to-epaas'].on_page_load = function(wrapper) {
	var parent = $('<div class="welcome-to-epaas"></div>').appendTo(wrapper);

	parent.html(dataent.render_template("welcome_to_epaas", {}));

	parent.find(".video-placeholder").on("click", function() {
		window.epaas_welcome_video_started = true;
		parent.find(".video-placeholder").addClass("hidden");
		parent.find(".embed-responsive").append('<iframe class="embed-responsive-item video-playlist" src="https://www.youtube.com/embed/videoseries?list=PL3lFfCEoMxvxDHtYyQFJeUYkWzQpXwFM9&color=white&autoplay=1&enablejsapi=1" allowfullscreen></iframe>')
	});

	// pause video on page change
	$(document).on("page-change", function() {
		if (window.epaas_welcome_video_started && parent) {
			parent.find(".video-playlist").each(function() {
				this.contentWindow.postMessage('{"event":"command","func":"' + 'pauseVideo' + '","args":""}', '*');
			});
		}
	});
}
