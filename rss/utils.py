import feedparser as fp
from django.contrib import messages

## called by parse_url view
def extract_headers(request, url):
    # check if it is a valid rss or not
    # if not, give a message
    # if yes, add in database and send message
    newsfeed = fp.parse(url)
    if newsfeed.bozo==True:
        if newsfeed.bozo_exception.reason.errno==11001:
            messages.error(request, "Unable to parse URL.. Please check if you enterd a valid URL")
            return None
    else:
        feed = newsfeed.feed
        feed_data = {
        "title": getattr(feed, "title", None),
        "description": getattr(feed, "subtitle", None),
        "author": getattr(feed, "author", None),
        "logo": getattr(getattr(feed, "image", None), "href", None)
        }
        feed_data.update({"url":url, "category":None, "public": False, "custom":True})
        messages.success(request, "RSS has been added to your subscriptions")
        print(feed_data, end="\n\n")

        ## automatic subscribing for the custom url
        if not RssFeed.objects.filter(url=url).exists():
            new_feed = RssFeed.objects.create(**feed_data)
            # models.Subscriptions.objects.create(user=request.user, )
            print(new_feed.id, new_feed.url)

    return (feed_data)