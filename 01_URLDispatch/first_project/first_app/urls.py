from django.urls import path
from . import views

app_name = 'first_app'

urlpatterns = [
    path('hello', views.index, name='index'),
    path('page/<str:user_name>', views.user_page, name='user_page'),
    path('number_page/<str:user_name>/<int:number>', views.number_page, name='number_page'),
]