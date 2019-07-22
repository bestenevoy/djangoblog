from django.shortcuts import render, reverse, redirect
from django.views import View
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponse
from .forms import LoginForm, RegisterForm, ChangePasswordForm, ChangeNicknameForm
from .models import User
import random
import string
import time


# Create your views here.

# 用户资料编辑：编辑完成后转到用户资料查看页面

# 用户注册: 注册完成后转到登录页面
# /user/register/
class RegisterView(View):
    '''用户注册'''

    def get(self, request):
        '''注册页面显示'''
        register_form = RegisterForm()
        context = {}
        context['register_form'] = register_form
        return render(request, 'user/register.html', context)

    def post(self, request):
        '''实现用户注册'''
        register_form = RegisterForm(request.POST, request=request)
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            email = register_form.cleaned_data['email']
            password = register_form.cleaned_data['password']
            user = User.objects.create_user(username, email, password)
            user.save()

            # 清除session
            del request.session['register_code']

            # 登陆用户
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect(request.GET.get('from', reverse('blog:home')))
        context = {}
        context['register_form'] = register_form
        return render(request, 'user/register.html', context)


# 用户登陆
# /user/login/
class LoginView(View):
    def get(self, request):
        login_form = LoginForm()
        context = {}
        context['form'] = login_form
        return render(request, 'user/login.html', context)

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            login(request, user)
            return redirect(request.GET.get('from', reverse('blog:home')))
        context = {}
        context['login_form'] = login_form
        referer = request.META.get('HTTP_REFERER', reverse('blog:home'))
        return render(request, 'user/login.html', context)


# /user/logout/
class LogoutView(View):
    def get(self, request):
        logout(request)
        referer = request.META.get('HTTP_REFERER', reverse('blog:home'))
        return redirect(referer)


# 用户资料页面: 查看用户注册信息，并提供编辑资料按钮
# /user
class UserInfoView(LoginRequiredMixin, View):
    def get(self, request):
        context = {}
        return render(request, 'user/user_info.html', context)


# 修改昵称
# /user/change_nickname/
class ChangeNicknameView(LoginRequiredMixin, View):
    def get(self, request):
        change_nickname_form = ChangeNicknameForm()
        context = {}
        context['form'] = change_nickname_form
        return render(request, 'user/change_nickname.html', context)

    def post(self, request):
        nickname_form = ChangeNicknameForm(request.POST)
        if nickname_form.is_valid():
            nickname = nickname_form.cleaned_data['nickname']
            user = request.user
            user.nickname = nickname
            user.save()
        return redirect(reverse('user:info'))


# 用户密码重置
class ChangePasswordView(LoginRequiredMixin, View):
    def get(self, request):
        change_password_form = ChangePasswordForm()
        context = {}
        context['form'] = change_password_form
        return render(request, 'user/change_password.html', context)

    def post(self, request):
        user = request.user
        change_pw_form = ChangePasswordForm(request.POST, user=user)
        if change_pw_form.is_valid():
            new_password = change_pw_form.cleaned_data['new_password']
            user.set_password(new_password)
            user.save()
        return redirect(reverse('user:info'))


# 发送验证码
# /user/send_email_code
def send_email_code(request):
    to_email = request.GET.get('to_email', '')
    send_for = request.GET.get('send_for', '')
    verify_code = ''.join(random.sample(string.ascii_letters + string.digits, 4))

    if to_email == '':
        return JsonResponse({'res': 0, 'errmsg': '邮箱不能为空'})

    if User.objects.filter(email=to_email).exists():
        return JsonResponse({'res': 1, 'errmsg': '邮箱已存在'})
    import re
    patterns = re.compile(r'^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$')
    if not patterns.match(to_email):
        return JsonResponse({'res': 2, 'errmsg': '验证码格式不正确'})
    # 判断发送时间
    now_time = int(time.time())
    send_code_time = request.session.get('send_code_time', 0)
    if now_time - send_code_time < 30:
        return JsonResponse({'res': 3, 'errmsg': 'ERROR'})

    # 发送邮件
    subject = 'WRZ的个人博客'  # 主题
    # 邮件正文
    message = ''
    # 如果内容含有 HTML格式 则不能通过 message 传参，需要通过 html_massage 传参，解析为 html文档
    html_message = '<h1>欢迎您</h1><br>验证码：%s' % (verify_code)
    sender = settings.EMAIL_FROM  # 发件人
    recipient_list = [to_email]  # 收件人
    send_mail(subject, message, sender, recipient_list, html_message=html_message)

    # todo: 保存注册码、邮箱信息和发送时间
    request.session[send_for] = verify_code
    request.session['send_to_email'] = to_email
    request.session['send_code_time'] = now_time
    return JsonResponse({'res': 4, 'massage': '已发送'})
