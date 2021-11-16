from django.urls import path
from . import views

app_name='first'

urlpatterns = [
    path('add/<int:num1>/<int:num2>', views.add, name='add'),
    path('minus/<str:num1>/<str:num2>', views.minus, name='minus'),
    path('div/<str:num1>/<str:num2>', views.div, name='div'),
]