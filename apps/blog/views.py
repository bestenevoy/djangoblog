from django.shortcuts import render, get_object_or_404
from django.views import View
from django.contrib.contenttypes.models import ContentType
# API
from rest_framework.parsers import JSONParser
from .serializers import ArticleSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Article, Category
from comment.models import Comment
from comment.forms import CommentForm
from utils.paginator import paginator

# Create your views here.

# localhost:8000/
class HomeView(View):
    '''首页显示'''

    def get(self, request):
        return render(request, 'home.html')


# localhost:8000/article/blog_id
class ArticleDetailView(View):
    '''文章详情'''

    def get(self, request, article_pk):
        # 使用 django 自带函数，如果请求的模型对象不存在，抛出 HTTP404
        article = get_object_or_404(Article, pk=article_pk)  # 不知道主键名称，可以写 pk
        if not request.COOKIES.get('article_%s_read' % article_pk):
            article.views += 1
            article.save()

        previous_article = Article.objects.filter(created_time__gt=article.created_time).last()
        next_article = Article.objects.filter(created_time__lt=article.created_time).first()
        article_model = ContentType.objects.get_for_model(Article)
        comments = Comment.objects.filter(content_type=article_model, object_id=article_pk)
        # 组织模版上下文
        context = {}
        context['previous_article'] = previous_article
        context['next_article'] = next_article
        context['article'] = article
        context['comments'] = comments
        context['comments_form'] = CommentForm(initial={'content_type': article_model.model,
                                                        'object_id': article_pk,})
        response = render(request, 'blog/article.html', context)
        response.set_cookie('article_%s_read' % article_pk, 'true', max_age=24 * 3600)
        return response


# localhost:8000/article
class ArticleListView(View):
    '''显示全部文章列表'''

    def get(self, request):
        articles = Article.objects.all()
        articles_of_page, page_range = paginator(request, articles, 2)
        context = {}
        context['articles_of_page'] = articles_of_page
        context['page_range'] = page_range
        context['article_by_dates'] = Article.objects.dates('created_time', 'month', order='DESC')
        context['categorys'] = Category.objects.all().order_by('index')

        return render(request, 'blog/article_list.html', context)


# 类别文章详情页
class CategoryDetailView(View):
    def get(self, request, category_pk):
        category = get_object_or_404(Category, pk=category_pk)
        articles = Article.objects.filter(category=category)
        page = request.GET.get('page', 1)

        articles_of_page, page_range = paginator(request, articles, 10)
        context = {}
        context['category'] = category
        context['articles_of_page'] = articles_of_page
        context['page_range'] = page_range
        context['article_by_dates'] = Article.objects.dates('created_time', 'month', order='DESC')
        context['categorys'] = Category.objects.all().order_by('index')
        return render(request, 'blog/category_detail.html', context)


# 按年月分类显示
class SortByDateView(View):
    def get(self, request, year, month):
        articles = Article.objects.filter(created_time__year=year, created_time__month=month)
        articles_of_page, page_range = paginator(request, articles, 5)
        context = {}
        context['date_time'] = '%s年%s月' % (year, month)
        context['articles_of_page'] = articles_of_page
        context['page_range'] = page_range
        context['article_by_dates'] = Article.objects.dates('created_time', 'month', order='DESC')
        context['categorys'] = Category.objects.all().order_by('index')

        return render(request, 'blog/article_sort_by_date.html', context)


class ApiView(APIView):
    """
    List all code blog.
    """

    def get(self, request, format=None):
        # 1. api 可以用 Json serializers 来实现

        # blogs = Blog.objects.all()
        # from django.core.serializers import serialize
        # data = serialize('json',blogs)
        # from django.http import JsonResponse
        # return JsonResponse(data,safe=False)

        # 使用 DRF
        # 将 settings.py REST_FRAMEWORK 中的 身份验证注释
        blogs = Article.objects.all()
        serializer = ArticleSerializer(blogs, many=True)
        return Response(serializer.data)
