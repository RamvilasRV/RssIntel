from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.contrib import messages
import feedparser as fp


from .models import RssFeed, Subscriptions
# from .utils import extract_headers

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

def subscribe(request):
    if request.method == "POST":
        url = request.POST.get("url")
        subscribe_to_feed(request, url)
    return redirect("discover")


## called by parse_url view
def extract_headers(request, url):
    # check if it is a valid rss or not
    # if not, give a message
    # if yes, add in database and send message
    ### WHY DONT WE FIRST CHECK IF THE URL ALREADY EXISTS IN THE USERS SUBSRIPTIONS OR NOT?###
    ### BUT IN A GENERAL USECASE, A PERSON WILL ONLY ADD IT ONCE AND THE USER TRYING TO ADD A URL TWICE IS PRETTY RARE, HENCE WHY SIMPLY ADD A LOGIC TO CHECK FOR IT??###
    ### BUT WHAT HAPPENS WHEN THE USER TRIES TO DO SO?###
    ### WE ARE ANYWAY VALIDATING THE SUBS TABLE LATER, HENCE FUNCNTION WISE, THERE IS NO ISSUE. BUT THE QUESTION IS WHY DO WE ADD ADTIONAL CHECKS FOR THE A THING THAT IS SUPPOSED TO HAPPEN VERY RARELY (IN AN IDEAL SITUATION, OF COURSE) ###


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
        # messages.success(request, "RSS has been added to your subscriptions")
        print(feed_data, end="\n\n")

        if not RssFeed.objects.filter(url=url).exists():
            new_feed = RssFeed.objects.create(**feed_data)
            print(new_feed.id, new_feed.url)

        subscribe_to_feed(request, url)
        # print(type(url))

    return (feed_data)


## A general function for subscribing to the feed.
def subscribe_to_feed(request, url):
    rss_feed = RssFeed.objects.get(url=url)

    if not Subscriptions.objects.filter(user=request.user, rss_feed=rss_feed).exists():
        Subscriptions.objects.create(user=request.user, rss_feed=rss_feed)
        messages.success(request, "You have been subscribed to this feed.")
    else:
        messages.error(request, "You have already subscribed to this feed.")

    return None


class SubscriptionsListView(ListView):
    model = Subscriptions
    template_name = "rss/subscription_list.html"
    context_object_name = 'subscriptions'

    def get_queryset(self):
        return Subscriptions.objects.filter(user=self.request.user)

def read_rss(request,id):
    subscription = Subscriptions.objects.get(id=id, user=request.user)
    url = Subscriptions.rss_feed.url
    parse_rss(url)
    return render(request, "read_rss.html")


def parse_rss(url):
    feed = fp.parse(url)

    entries = feed.entiries

    for i in entries:
        ## build list of dictionaries