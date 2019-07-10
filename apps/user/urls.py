# -*- coding:utf-8 -*-
__author__ = 'wrz'
__data__ = '2019/6/1 1:49'

from django.urls import path
from .views import RegisterView, LoginView, LogoutView, UserInfoView, ChangePasswordView, ChangeNicknameView
from .views import send_email_code

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('send_email_code',send_email_code , name='send_email_code'), # 发送验证码
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('',UserInfoView.as_view(), name='info'),
    path('change_nickname/',ChangeNicknameView.as_view(), name='change_nickname'),
    path('change_pw/',ChangePasswordView.as_view(), name='change_password'),
]