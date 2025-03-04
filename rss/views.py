from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from . import models

# Create your views here.

@method_decorator(login_required(login_url='/users/login/'), name='dispatch')
class Discover(LoginRequiredMixin, ListView):
    model = models.RssFeed
    template_name = "rss/discover.html"
    context_object_name = "rsss"
    paginate_by = 5