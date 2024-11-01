from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserForm, UserLoginForm, RequestPasswordResetForm, SetNewPasswordForm
from .models import PasswordResetToken
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import uuid

def user_list(request):
    return render(
        request, 'user/user_list.html'
    )

def regist(request):
    # user_form = UserForm(request.POST or None)
    # if user_form.is_valid():
    #     user = user_form.save(commit=False)
    #     password = user_form.cleaned_data.get('password', '')
    #     try:
    #         validate_password(password)
    #     except ValidationError as e:
    #         user_form.add_error('password', e)
    #         return render(request, 'user/registration.html', context={
    #             'user_form': user_form,
    #         })
    #     user.set_password(password)
    #     user.save()
    user_form = UserCreationForm(request.POST or None)
    if user_form.is_valid():
        user_form.save()
    return render(request, 'user/registration.html', context={
        'user_form': user_form,
    })

def login_view(request):
    login_form = UserLoginForm(request.POST or None)
    next_url = request.GET.get('next')
    if login_form.is_valid():
        username = login_form.cleaned_data.get('username')
        password = login_form.cleaned_data.get('password1')
        # 認証処理（成功したらuserが返される）
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_authenticated:
            login(request, user)# ログイン処理
            redirect_url = next_url if next_url else 'user:index'
            return redirect(redirect_url)
        else:
            login_form.add_error('username', '認証に失敗しました')
    return render(request, 'user/login.html', context={
        'login_form': login_form,
    })

def index(request):
    print(request.user)
    return render(request, 'user/index.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('user:login')

@login_required
def info(request):
    return render(request, 'user/info.html')

def request_password_reset(request):
    form = RequestPasswordResetForm(request.POST or None)
    message = ''
    if form.is_valid():
        email = form.cleaned_data['email']
        user = get_object_or_404(User, email=email)
        # 新しいトークンを作成
        password_reset_token, created = PasswordResetToken.objects.get_or_create(user=user)
        if not created:
            password_reset_token.token = uuid.uuid4()
            password_reset_token.used = False
            password_reset_token.save()
        user.is_active = False
        user.save()
        token = password_reset_token.token
        print(f"{request.scheme}://{request.get_host()}/user/reset_password/{token}")
        message = 'パスワードリセットトークンをお送りしました'
    return render(request, 'user/password_reset_form.html', context={
        'reset_form': form, 'message': message,
    })

def reset_password(request, token):
    password_reset_token = get_object_or_404(
        PasswordResetToken,
        token=token,
        used=False,
    )
    form = SetNewPasswordForm(request.POST or None)
    message = ''
    if form.is_valid():
        user = password_reset_token.user
        password = form.cleaned_data['password1']
        validate_password(password)
        # パスワード更新
        user.set_password(password)
        user.is_active = True
        user.save()
        
        password_reset_token.used = True
        password_reset_token.save()
        message = 'パスワードをリセットしました。'
    
    return render(request,'user/password_reset_confirm.html', context={
        'form': form, 'message': message,
    })
    