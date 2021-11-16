from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('item_list/', views.item_list, name='item_list'),
    path('item_detail/<int:id>', views.item_detail, name='item_detail'),
    path('to_google/', views.to_google, name='to_google'),
    path('one_item/', views.one_item, name='one_item'),
]