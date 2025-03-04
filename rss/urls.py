from django.urls import path
from . import views

urlpatterns = [
    path('discover/', views.Discover.as_view(), name='discover')
]