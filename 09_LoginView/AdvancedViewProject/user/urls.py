from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('user_list/', views.user_list, name='user_list'),
    path('regist/', views.regist, name='regist'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('index/', views.index, name='index'),
    path('info/', views.info, name='info'),
    path('request_password_reset/', views.request_password_reset, name='request_password_reset'),
    path('reset_password/<uuid:token>/', views.reset_password, name='reset_password'),
]
