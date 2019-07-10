from django.shortcuts import render, redirect, reverse
from django.views import View
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from .models import Comment
from .forms import CommentForm
# Create your views here.
class CommentView(View):
    def post(self,request):
        '''
        提交评论内容
        :param request:
        :return: 从定向到评论内容页面
        '''
        data = {}
        user = request.user
        comment_form = CommentForm(request.POST, user=user)
        if not comment_form.is_valid():
            return JsonResponse(data=data)
        comment = Comment()
        comment.content_object=comment_form.cleaned_data['content_object']
        comment.user = comment_form.cleaned_data['user']
        comment.body = comment_form.cleaned_data['body']
        comment.root = comment_form.cleaned_data['root']
        comment.parent = comment_form.cleaned_data['parent']
        comment.save()
        referer = request.META.get('HTTP_REFERER',reverse('blog:home'))
        return redirect(referer)