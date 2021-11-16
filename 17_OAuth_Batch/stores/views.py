from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from django.views.generic.base import TemplateView
from django.views.generic.edit import (
    UpdateView, DeleteView, CreateView
)
from django.urls import reverse_lazy
from django.core.cache import cache
from django.db import transaction

import os
from .models import(
    Addresses, Products, Carts, CartItems,
    Orders, OrderItems,
)
from .forms import(
    CartUpdateForm, AddressInputForm,
)

class ProductListView(LoginRequiredMixin, ListView):
    model = Products
    template_name = os.path.join('stores', 'product_list.html')

    def get_queryset(self):
        query = super().get_queryset()
        product_type_name = self.request.GET.get('product_type_name', None)
        product_name = self.request.GET.get('product_name', None)
        if product_type_name:
            query = query.filter(
                product_type__name=product_type_name
            )
        if product_name:
            query = query.filter(
                name=product_name
            )
        order_by_price = self.request.GET.get('order_by_price', 0)
        if order_by_price == '1':
            query = query.order_by('price')
        elif order_by_price == '2':
            query = query.order_by('-price')
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_type_name'] = self.request.GET.get('product_type_name', '')
        context['product_name'] = self.request.GET.get('product_name', '')
        order_by_price = self.request.GET.get('order_by_price', 0)
        if order_by_price == '1':
            context['ascending'] = True
        elif order_by_price == '2':
            context['descending'] = True
        return context


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Products
    template_name = os.path.join('stores', 'product_detail.html')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_added'] = CartItems.objects.filter(
            cart_id=self.request.user.id,
            product_id=kwargs.get('object').id
        ).first()
        return context

@login_required
def add_product(request):
    if request.is_ajax:
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')
        product = get_object_or_404(Products, id=product_id)
        if int(quantity) > product.stock:
            response = JsonResponse({'message': '在庫数を超えています'})
            response.status_code = 403
            return response
        if int(quantity) <= 0:
            response = JsonResponse({'message': '0より大きい値を入力してください'})
            response.status_code = 403
            return response
        cart = Carts.objects.get_or_create(
            user=request.user
        )
        if all([product_id, cart, quantity]):
            CartItems.objects.save_item(
                quantity=quantity, product_id=product_id,
                cart=cart[0]
            )
            return JsonResponse({'message': '商品をカートに追加しました'})


class CartItemsView(LoginRequiredMixin, TemplateView):
    template_name = os.path.join('stores', 'cart_items.html')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.user.id
        query = CartItems.objects.filter(cart_id=user_id)
        total_price = 0
        items = []
        for item in query.all():
            total_price += item.quantity * item.product.price
            picture = item.product.productpictures_set.first()
            picture = picture.picture if picture else None
            in_stock = True if item.product.stock >= item.quantity else False
            tmp_item = {
                'quantity': item.quantity,
                'picture': picture,
                'name': item.product.name,
                'id': item.id,
                'price': item.product.price,
                'in_stock': in_stock,
            }
            items.append(tmp_item)
        context['total_price'] = total_price
        context['items'] = items
        return context


class CartUpdateView(LoginRequiredMixin, UpdateView):
    template_name = os.path.join('stores', 'update_cart.html')
    form_class = CartUpdateForm
    model = CartItems
    success_url = reverse_lazy('stores:cart_items')


class CartDeleteView(LoginRequiredMixin, DeleteView):
    template_name = os.path.join('stores', 'delete_cart.html')
    model = CartItems
    success_url = reverse_lazy('stores:cart_items')


class InputAddressView(LoginRequiredMixin, CreateView):
    template_name = os.path.join('stores', 'input_address.html')
    form_class = AddressInputForm
    success_url = reverse_lazy('stores:confirm_order')

    def get(self, request, pk=None):
        cart = get_object_or_404(Carts, user_id=request.user.id)
        if not cart.cartitems_set.all():
            raise Http404('商品が入っていません')
        return super().get(request, pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        address = cache.get(f'address_user_{self.request.user.id}')
        pk = self.kwargs.get('pk')
        address = get_object_or_404(Addresses, user_id=self.request.user.id, pk=pk) if pk else address
        if address:
            context['form'].fields['zip_code'].initial = address.zip_code
            context['form'].fields['prefecture'].initial = address.prefecture
            context['form'].fields['address'].initial = address.address
        context['addresses'] = Addresses.objects.filter(user=self.request.user).all()
        return context

    def form_valid(self, form):
        form.user = self.request.user
        return super().form_valid(form)


class ConfirmOrderView(LoginRequiredMixin, TemplateView):
    template_name = os.path.join('stores', 'confirm_order.html')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        address = cache.get(f'address_user_{self.request.user.id}')
        context['address'] = address
        cart = get_object_or_404(Carts, user_id=self.request.user.id)
        context['cart'] = cart
        total_price = 0
        items = []
        for item in cart.cartitems_set.all():
            total_price += item.quantity * item.product.price
            picture = item.product.productpictures_set.first()
            picture = picture.picture if picture else None
            tmp_item = {
                'quantity': item.quantity,
                'picture': picture,
                'name': item.product.name,
                'price': item.product.price,
                'id': item.id,
            }
            items.append(tmp_item)
        context['total_price'] = total_price
        context['items'] = items
        return context
    
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        address = context.get('address')
        cart = context.get('cart')
        total_price = context.get('total_price')
        if (not address) or (not cart) or (not total_price):
            raise Http404('注文処理でエラーが発生しました')
        for item in cart.cartitems_set.all():
            if item.quantity > item.product.stock:
                raise Http404('注文処理でエラーが発生しました')
        order = Orders.objects.insert_cart(cart, address, total_price)
        OrderItems.objects.insert_cart_items(cart, order)
        Products.objects.reduce_stock(cart)
        cart.delete()
        return redirect(reverse_lazy('stores:order_success'))


class OrderSuccessView(LoginRequiredMixin, TemplateView):

    template_name = os.path.join('stores', 'order_success.html')
