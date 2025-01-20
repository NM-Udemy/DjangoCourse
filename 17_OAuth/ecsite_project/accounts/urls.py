from django.urls import path
from .views import (
    RegistUserView, HomeView, UserLoginView,
    UserLogoutView, UserView, UserLoginView2,
    UserLogoutView2, google_callback, google_login
)

app_name = 'accounts'
urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('regist/', RegistUserView.as_view(), name='regist'),
    path('user_login/', UserLoginView.as_view(), name='user_login'),
    path('user_logout/', UserLogoutView.as_view(), name='user_logout'),
    path('user/', UserView.as_view(), name='user'),
    path('user_login_2/', UserLoginView2.as_view(), name='user_login_2'),
    path('user_logout_2/', UserLogoutView2.as_view(), name='user_logout_2'),
    path('google/login/', google_login, name='google_login'),
    path('google/login/callback/', google_callback, name='google_callback'),
]