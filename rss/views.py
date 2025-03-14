from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.contrib import messages

import feedparser as fp

from .models import RssFeed, Subscriptions

# Create your views here.

@method_decorator(login_required(login_url='/users/login/'), name='dispatch')
class Discover(LoginRequiredMixin, ListView):
    model = RssFeed
    template_name = "rss/discover.html"
    context_object_name = "rsss"
    paginate_by = 5

def parse_url(request):
    if request.method=="POST":
        url = request.POST.get('url')
        extract_headers(request, url)
    return redirect("discover")


## called by parse_url
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

        if not RssFeed.objects.filter(url=url).exists():
            new_feed = RssFeed.objects.create(**feed_data)
            # models.Subscriptions.objects.create(user=request.user, )
            print(new_feed.id, new_feed.url)



    return (feed_data)