import feedparser as fp

url = "https://timesofindia.indiatimes.com/rssfeedstopstories.cms"

# url = "https://feeds.feedburner.com/ndtvnews-top-stories"

feed = fp.parse(url)

entries = feed.entries


def get_enclosures(entry, to_search, name):
	"""gets all the enclosure links from the enclosure list"""
	result_list = []
	content_in_rss = (getattr(entry, to_search, []))
	if len(content_in_rss)!=0:
		for i in content_in_rss:
			result_list.append(i[name])
	return result_list


for entry in entries:
	## build list of dictionaries with following stuff
	"""
	published
	author 
	publisher
	summary
	content
	enclosures
	link
	"""
	entries_data = {
	"published": getattr(entry, "published", None),
	"author": getattr(entry, "author", None),
	"publisher": getattr(entry, "publisher", None),
	"summary": getattr(entry, "summary", None),
	"contents": get_enclosures(entry,"content", "value"),
	"enclosures": get_enclosures(entry, "enclosures", "href"),
	"link": getattr(entry, "link", None)
	}

	print(getattr(entry, "enclosures", None))

### Need to extract the enclosures
### Display enclosures on the top, before the content
