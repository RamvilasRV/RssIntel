import feedparser as fp

links = ["https://feeds.feedburner.com/ndtvnews-top-stories",
		 "https://www.livemint.com/rss/companies",
		 "https://timesofindia.indiatimes.com/rssfeedstopstories.cms",
		 "https://feeds.bbci.co.uk/news/rss.xml",
		 "https://meanttodie.com"]


feed_fields = ["title", "author", "icon", "link", "logo", "subtitle", "tags", "image", ]

feed_info = []

for link in links:
	newsfeed = fp.parse(link)
	if newsfeed.bozo==True:
		if newsfeed.bozo_exception.reason.errno==11001:
			print("Unable to parse URL.. Please check if you enterd a valid URL")
	# elif articles_empty:

	else:
		feed = newsfeed.feed

		### USing lambda
		# attributes = {
		# 	"title": lambda x: x.title,
		# 	"subtitle": lambda x: x.subtitle,
		# 	"image" : lambda x: x.image.href,
		# 	"author": lambda x: x.author
		# }

		### WORST WAY
		# for i in attributes:
		# attrs = ["title", "subtitle", "image", "author"]
		# if 'title' in newsfeed.feed:
		# 	print(newsfeed.feed.title)
		# if 'subtitle' in newsfeed.feed:
		# 	print(newsfeed.feed.subtitle)
		# if 'image' in newsfeed.feed:
		# 	print(newsfeed.feed.image.href)
		# if 'author' in newsfeed.feed:
		# 	print(newsfeed.feed.author)

		### Using gettar()
		feed_data = {
		"title": getattr(feed, "title", None),
		"subtitle": getattr(feed, "subtitle", None),
		"author": getattr(feed, "author", None),
		"image": getattr(getattr(feed, "image", None), "href", None)
		}

	print(feed_data, end="\n\n")
		

"""title, subtitle, image, author """
