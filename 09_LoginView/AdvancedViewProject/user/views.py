from django.shortcuts import render, redirect
from django.http import HttpResponse
from user.forms import UserForm, ProfileForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

# Create your views here.
def user_list(request):
    return render(request, 'user/user_list.html')

def index(request):
    return render(request, 'user/index.html')

def register(request):
    user_form = UserForm(request.POST or None)
    profile_form = ProfileForm(request.POST or None, request.FILES or None)
    if user_form.is_valid() and profile_form.is_valid():
        user = user_form.save(commit=False)
        try:
            validate_password(user_form.cleaned_data.get('password'), user)
        except ValidationError as e:
            user_form.add_error('password', e)
            return render(request, 'user/registration.html', context={
                'user_form': user_form,
                'profile_form': profile_form,
            })
        user.set_password(user.password)
        user.save() # ユーザを保存
        profile = profile_form.save(commit=False)
        profile.user = user
        profile.save()
    return render(request, 'user/registration.html', context={
        'user_form': user_form,
        'profile_form': profile_form,
    })


def user_login(request):
    login_form = LoginForm(request.POST or None)
    if login_form.is_valid():
        username = login_form.cleaned_data.get('username')
        password = login_form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('user:index')
            else:
                return HttpResponse('アカウントがアクティブでないです')
        else:
            return HttpResponse('ユーザが存在しません')
    return render(request, 'user/login.html', context={
        'login_form': login_form
    })

@login_required
def user_logout(request):
    logout(request)
    return redirect('user:index')

@login_required
def info(request):
    return HttpResponse('ログインしています')
