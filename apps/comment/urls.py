from django.urls import path
from django.contrib.auth.decorators import login_required
from django.conf.urls import url

from .views import CommentView
urlpatterns = [
    path('', login_required(CommentView.as_view()), name='comment'),
]
