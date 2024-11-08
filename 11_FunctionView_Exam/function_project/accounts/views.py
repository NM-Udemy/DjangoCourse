from django.shortcuts import render, redirect
from . import forms
from .models import UserActivateToken
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required

def home(request):
    return render(
        request, 'accounts/home.html'
    )

def regist(request):
    regist_form = forms.RegistForm(request.POST or None)
    if regist_form.is_valid():
        regist_form.save(commit=True)
        return redirect('accounts:home')
    return render(
        request, 'accounts/regist.html', context={
            'regist_form': regist_form,
        }
    )
    
def activate_user(request, token):
    activate_form = forms.UserActivateForm(request.POST or None)
    if activate_form.is_valid():
        UserActivateToken.objects.activate_user_by_token(token) # ユーザー有効化
        messages.success(request, 'ユーザーを有効化しました')
    activate_form.initial['token'] = token
    return render(
        request, 'accounts/activate_user.html', context={
            'activate_form': activate_form,
        }
    )
    
def user_login(request):
    login_form = forms.LoginForm(request.POST or None)
    if login_form.is_valid():
        email = login_form.cleaned_data['email']
        password = login_form.cleaned_data['password']
        user = authenticate(email=email, password=password)
        if user:
            login(request, user)
            next_url = request.GET.get('next', 'accounts:home')
            return redirect(next_url)
        else:
            messages.warning(request, 'ログインに失敗しました')
    return render(
        request, 'accounts/user_login.html', context={
            'login_form': login_form,
        }
    )

@login_required
def user_logout(request):
    logout(request)
    return redirect('accounts:home')

@login_required
def user_edit(request):
    user_edit_form = forms.UserEditForm(
        request.POST or None, request.FILES or None, instance=request.user
    )
    if user_edit_form.is_valid():
        user_edit_form.save()
        messages.success(request, '更新完了しました')
    return render(request, 'accounts/user_edit.html', context={
        'user_edit_form': user_edit_form,
    })

@login_required
def change_password(request):
    password_change_form = forms.PasswordChangeForm(
        request.POST or None, instance=request.user
    )
    if password_change_form.is_valid():
        password_change_form.save(commit=True)
        messages.success(request, 'パスワード更新しました')
        update_session_auth_hash(request, request.user)
    return render(
        request, 'accounts/change_password.html', context={
            'password_change_form': password_change_form,
        }
    )

def show_error_page(request, exception):
    return render(
        request, '404.html'
    )
