from django.urls import path
from . import views

urlpatterns = [
    path('discover/', views.Discover.as_view(), name='discover'),
    path('custom_url/', views.parse_url, name="parse_url"),
    path('subscribe/', views.subscribe, name="subscribe")
]