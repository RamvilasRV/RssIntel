def parse_feed(feed):
	feed_data = {
	"title": getattr(feed, "title", "No title available"),
	"description": getattr(feed, "subtitle", "No subtitle available"),
	"author": getattr(feed, "author", "No author available"),
	"logo": getattr(getattr(feed, "image", ""), "href", "No image available")
	}

	return feed_data