# -*- coding:utf-8 -*-
__author__ = 'wrz'
__data__ = '2019/7/4 21:21'

from django import forms
from django.contrib.contenttypes.models import ContentType
from django.db.models import ObjectDoesNotExist
from .models import Comment


class CommentForm(forms.Form):
    body = forms.CharField(label=False ,widget=forms.Textarea(attrs={'class':'form-control','rows':4, 'style':'display:none'}))
    root_id = forms.IntegerField(initial=0, widget=forms.HiddenInput(attrs={'id':'root_id'}))
    parent_id = forms.IntegerField(initial=0, widget=forms.HiddenInput(attrs={'id':'parent_id'}))

    content_type = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.IntegerField(widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean(self):
        # 1. 判断用户是否
        if not self.user.is_authenticated:
            raise forms.ValidationError('用户未登录')
        self.cleaned_data['user'] = self.user

        # 2. 判断评论内容是否为空
        body = self.cleaned_data['body']
        if not body:
            raise forms.ValidationError('内容不能为空')

        # 3. 验证评论对象是否存在
        content_type = self.cleaned_data['content_type']
        object_id = self.cleaned_data['object_id']
        try:
            content_model = ContentType.objects.get(model=content_type).model_class()
            content_object = content_model.objects.get(pk=object_id)
        except ObjectDoesNotExist:
            raise forms.ValidationError('评论对象不存在')
        self.cleaned_data['content_object'] = content_object

        return self.cleaned_data

    def clean_root_id(self):
        root_id = self.cleaned_data['root_id']
        if root_id < 0:
            raise forms.ValidationError('请求错误')
        elif root_id==0:
            self.cleaned_data['root'] = None
        else:
            try:
                root = Comment.objects.get(pk=root_id)
            except ObjectDoesNotExist:
                raise forms.ValidationError('评论对象不存在')
            self.cleaned_data['root'] = root
        return root_id

    def clean_parent_id(self):
        parent_id = self.cleaned_data['parent_id']
        if parent_id < 0:
            raise forms.ValidationError('请求错误')
        elif parent_id==0:
            self.cleaned_data['parent'] = None
        else:
            try:
                parent = Comment.objects.get(pk=parent_id)
            except ObjectDoesNotExist:
                raise forms.ValidationError('评论对象不存在')
            self.cleaned_data['parent'] = parent
        return parent_id