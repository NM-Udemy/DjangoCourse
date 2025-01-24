from django.urls import path
from .views import (
    ProductListView, ProductDetailView, CartItemView, CartTemplateView,
    AddressView, OrderProductView
)

app_name = 'stores'

urlpatterns = [
    path('product_list/', ProductListView.as_view(), name='product_list'),
    path('product_detail/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('cart_item/', CartItemView.as_view(), name='cart_item'),
    path('cart_template/', CartTemplateView.as_view(), name='cart_template'),
    path('address/', AddressView.as_view(), name='set_address'),
    path('order/', OrderProductView.as_view(), name='order_product'),
]