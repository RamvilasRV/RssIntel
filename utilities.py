import feedparser as fp

url = "https://every.to/superorganizers/feed.xml"

feed = fp.parse(url)

# for i in range(len(feed.entries)):
# 	print((feed.entries[i].keys()))	

# for i in feed.entries[0]:
# 	print(i, type(i))

for i in feed.entries[0]:
	print(i, feed.entries[0][i])