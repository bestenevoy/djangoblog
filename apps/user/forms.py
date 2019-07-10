# -*- coding:utf-8 -*-
__author__ = 'wrz'
__data__ = '2019/6/1 1:26'

from django import forms
from django.contrib.auth import authenticate

from .models import User


class LoginForm(forms.Form):
    username = forms.CharField(
        label='用户名或邮箱', required=True,
        widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': "username or email"})
    )
    password = forms.CharField(
        label='密码', required=True,
        widget=forms.PasswordInput(attrs={"class": "form-control", 'placeholder': "password", })
    )

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError('用户名或密码不正确')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data


class RegisterForm(forms.Form):
    username = forms.CharField(label='用户名', required=True, max_length=30, min_length=3,
                               widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': "username "}))
    email = forms.EmailField(label='邮箱', required=True,
                             widget=forms.EmailInput(attrs={"class": "form-control", 'placeholder': "email"}))
    verification_code = forms.CharField(label='验证码', required=False,
                                        widget=forms.TextInput(
                                            attrs={"class": "form-control", 'placeholder': "点击“发送验证码”发送到邮箱"}))
    password = forms.CharField(label='请输入密码', min_length=6,
                               widget=forms.PasswordInput(attrs={"class": "form-control", 'placeholder': "password", }))
    password_again = forms.CharField(label='请确认密码', min_length=6,
                                     widget=forms.PasswordInput(
                                         attrs={"class": "form-control", 'placeholder': "password", }))

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    def clean_verification_code(self):
        # 判断验证码
        code = self.request.session.get('register_code', '')
        to_email = self.request.session.get('send_to_email', '')
        verification_code = self.cleaned_data.get('verification_code', '')
        email = self.cleaned_data.get('email', '')
        if not (code != '' and code == verification_code):
            raise forms.ValidationError('验证码不正确')

        if not (to_email != '' and to_email == email):
            raise forms.ValidationError('邮箱错误！')
        return verification_code

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户已存在')
        return username

    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password != password_again:
            raise forms.ValidationError('密码不一致')
        if len(password_again) < 6:
            raise forms.ValidationError('密码长度太短')
        return password_again


class ChangeNicknameForm(forms.Form):
    nickname = forms.CharField(
        label='请输入新的昵称', required=True, max_length=15, min_length=2,
        widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': "enter new nickname", })
    )


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        label='旧密码', required=True,
        widget=forms.PasswordInput(attrs={"class": "form-control", 'placeholder': "Old Password", })
    )
    new_password = forms.CharField(
        label='新密码', required=True,
        widget=forms.PasswordInput(attrs={"class": "form-control", 'placeholder': "New Password", })
    )
    new_password_again = forms.CharField(
        label='请再次输入新密码', required=True,
        widget=forms.PasswordInput(attrs={"class": "form-control", 'placeholder': "Reconfirmation", })
    )

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean(self):
        new_password = self.cleaned_data['new_password']
        new_password_again = self.cleaned_data['new_password_again']
        if new_password != new_password_again:
            raise forms.ValidationError('密码不一致')
        if len(new_password_again) < 6:
            raise forms.ValidationError('密码长度太短')
        self.cleaned_data['new_password'] = new_password
        return self.cleaned_data

    def clean_old_password(self):
        old_password = self.cleaned_data['old_password']

        if not self.user.check_password(old_password):
            raise forms.ValidationError('旧密码不正确')
        return old_password
