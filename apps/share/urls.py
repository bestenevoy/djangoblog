from django.urls import path
from django.contrib.auth.decorators import login_required
from django.conf.urls import url

from .views import *
urlpatterns = [
    path('', login_required(HomeView.as_view()),name='file_home'),
    url(r'^s/(?P<code>\d+)/$', DisplayView.as_view()),
    url(r'^search/', SearchView.as_view(), name="search"),
    url(r'^my/$', MyView.as_view(), name="MY")
]
