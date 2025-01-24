from django.shortcuts import render, redirect
from django.views.generic import(
    TemplateView, CreateView, FormView, View
)
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout, get_user_model
from .forms import RegistForm, UserLoginForm, UserLoginForm2, PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.password_validation import validate_password
import requests
import secrets, string

User = get_user_model()


class HomeView(TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        import os
        context['pid'] = os.getpid()
        return context

class RegistUserView(CreateView):
    template_name = 'regist.html'
    form_class = RegistForm
    success_url = reverse_lazy('accounts:home')

class UserLoginView(FormView):
    template_name = 'user_login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('accounts:home')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(email=email, password=password)
        if user:
            login(self.request, user)
        return super().form_valid(form)
    
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        print('next: ', next_url)
        return next_url if next_url else self.success_url

class UserLogoutView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'user_logout.html')

    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('accounts:home')


class UserLoginView2(LoginView):
    template_name = 'user_login_2.html'
    next_page = reverse_lazy('accounts:home')
    form_class = UserLoginForm2
    
    def form_valid(self, form):
        result = super().form_valid(form)
        print(self.request.user)
        remember = form.cleaned_data['remember']
        if remember:
            self.request.session.set_expiry(1200000)
        return result


class UserLogoutView2(LogoutView):
    next_page = reverse_lazy('accounts:home')
    http_method_names = ['get', 'post']
    template_name = 'user_logout.html'


class UserView(LoginRequiredMixin, FormView):
    template_name = 'user.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('accounts:home')
    
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
    
    def form_valid(self, form):
        user = self.request.user
        if isinstance(user, User):
            password = form.cleaned_data['password']
            validate_password(password, user)
            user.set_password(password)
            user.save()
            update_session_auth_hash(self.request, user)
            messages.success(self.request, 'パスワードを変更しました')
        return super().form_valid(form)


def google_login(request):
    """ Google認証画面に遷移 """
    oauth_url = 'https://accounts.google.com/o/oauth2/v2/auth'
    params = {
        'client_id': settings.GOOGLE_CLIENT_ID,
        'response_type': 'code',
        'scope': 'email profile',
        'redirect_uri': settings.GOOGLE_REDIRECT_URI,
        'prompt': 'select_acount'
    }
    param_string = '&'.join([f'{key}={value}' for key, value in params.items()])
    auth_url = f'{oauth_url}?{param_string}'
    print(auth_url)
    return redirect(auth_url)

def google_callback(request):
    """ Googleからのコールバック処理 """
    # 認可コードを取得
    code = request.GET.get('code')
    
    # アクセストークンの取得
    token_url = 'https://oauth2.googleapis.com/token'
    token_params = {
        'client_id': settings.GOOGLE_CLIENT_ID,
        'client_secret': settings.GOOGLE_CLIENT_SECRET,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': settings.GOOGLE_REDIRECT_URI
    }
    token_response = requests.post(token_url, data=token_params)
    token_data = token_response.json()
    access_token = token_data.get('access_token')
    
    # ユーザー情報の取得
    user_info_url = 'https://www.googleapis.com/oauth2/v2/userinfo'
    headers = {'Authorization': f'Bearer {access_token}'}
    user_info_response = requests.get(user_info_url, headers=headers)
    user_info = user_info_response.json()
    
    # ユーザーの取得、作成
    try:
        user = User.objects.get(email=user_info['email'])
    except User.DoesNotExist:
        password = ''.join(
            secrets.choice(
                string.ascii_letters + string.digits + string.punctuation
            ) for _ in range(32)
        )
        user = User.objects.create_user(
            username=user_info['name'],
            email=user_info['email'],
            password=password,
        )
        messages.info(request, 'パスワードを設定してください')
    login(request, user)
    return redirect('accounts:home') # ログイン後のリダイレクト先
