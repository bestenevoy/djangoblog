from django.urls import path
from django.conf.urls import url

from .views import HomeView, ArticleDetailView, ArticleListView, CategoryDetailView, SortByDateView, ApiView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),  # 首页
    path('article/<int:article_pk>.html', ArticleDetailView.as_view(), name='article'),  # 文章详情
    path('article.html',ArticleListView.as_view(),name='list'), #文章列表
    path('category/<int:category_pk>.html', CategoryDetailView.as_view(), name='category_detail'), # 类别文章详情
    path('date/<int:year>/<int:month>',SortByDateView.as_view(),name='sortbydate'),
    path('api/',ApiView.as_view(),name='api'),
]
