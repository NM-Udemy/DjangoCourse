from django.shortcuts import render, redirect
from django.views.generic import (
    ListView, DetailView, View, TemplateView, FormView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, Http404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import transaction

from .models import(
    Product, Cart, CartItem, Address, Order, OrderItem
)
from .forms import OrderForm
import json

class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'stores/product_list.html'
    context_object_name = 'products'
    paginate_by = 10
    ordering = ['id']
    
    def get_queryset(self):
        query = super().get_queryset()
        product_type_name = self.request.GET.get('product_type_name')
        product_name = self.request.GET.get('product_name')
        if product_type_name:
            query = query.filter(
                product_type__name=product_type_name
            )
        if product_name:
            query = query.filter(
                name=product_name
            )
        order_by_price = self.request.GET.get('order_by_price', '0')
        if order_by_price == '1':
            query = query.order_by('price')
        elif order_by_price == '2':
            query = query.order_by('-price')
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_type_name'] = self.request.GET.get('product_type_name', '')
        context['product_name'] = self.request.GET.get('product_name', '')
        order_by_price = self.request.GET.get('order_by_price', '0')
        context['order_by_price'] = order_by_price
        context['ascending'] = order_by_price == '1'
        context['descending'] = order_by_price == '2'
        return context


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'stores/product_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_item = CartItem.objects.filter(
            cart__user=self.request.user,
            product=self.object # type: ignore
        ).first()
        context['is_added'] = bool(cart_item)
        context['cart_quantity'] = cart_item.quantity if cart_item else None
        return context


@method_decorator(csrf_protect, name='dispatch')
class CartItemView(LoginRequiredMixin, View):
    http_method_names = ['post', 'put', 'delete']
    
    def validate_request(self, request):
        if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse(
                {'message': 'リクエストが不正です'},
                status=400
            )

    def validate_quantity(self, quantity, product):
        try:
            quantity = int(quantity)
        except ValueError:
            return JsonResponse(
                {'message': 'リクエストが不正です'},
                status=400
            )
        if quantity > product.stock:
            return JsonResponse(
                {'message': '在庫数を超えています'},
                status=400
            )
        if quantity <= 0:
            return JsonResponse(
                {'message': '0より大きい値を設定してください'},
                status=400
            )
        return quantity
    
    def post(self, request, *args, **kwargs):
        error_message = self.validate_request(request)
        if error_message:
            return error_message
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = data.get('quantity')
        
        product = get_object_or_404(Product, id=product_id)
        validated_quantity = self.validate_quantity(quantity, product)
        if isinstance(validated_quantity, JsonResponse):
            return validated_quantity

        cart, _ = Cart.objects.get_or_create(user=request.user)
        CartItem.objects.save_item(
            quantity=validated_quantity,
            product=product,
            cart=cart,
        )
        return JsonResponse({
            'message': '商品を追加しました。'
        })
        
    def put(self, request, *args, **kwargs):
        error_message = self.validate_request(request)
        if error_message:
            return error_message
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = data.get('quantity')
        
        product = get_object_or_404(Product, id=product_id)
        validated_quantity = self.validate_quantity(quantity, product)
        if isinstance(validated_quantity, JsonResponse):
            return validated_quantity
        
        cart = Cart.objects.get(user=request.user)
        cart_item = get_object_or_404(CartItem, cart=cart, product=product)
        cart_item.quantity = validated_quantity
        cart_item.save()

        return JsonResponse({
            'message': '商品を更新しました。'
        })
    
    def delete(self, request, *args, **kwargs):
        error_message = self.validate_request(request)
        if error_message:
            return error_message
        data = json.loads(request.body)
        product_id = data.get('product_id')
        
        product = get_object_or_404(Product, id=product_id)
        
        cart = Cart.objects.get(user=request.user)
        cart_item = get_object_or_404(CartItem, cart=cart, product=product)
        cart_item.delete()

        return JsonResponse({
            'message': '商品を削除しました。'
        })


class CartTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'stores/cart_item.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 商品情報、商品の全価格
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        total_price = 0
        cart_items = []
        
        for cart_item in cart.cart_items.select_related('product').all(): # type: ignore
            total_price += cart_item.quantity * cart_item.product.price
            picture = cart_item.product.pictures.first()
            picture = picture.picture if picture else None
            cart_items.append({
                'quantity': cart_item.quantity,
                'picture': picture,
                'name': cart_item.product.name,
                'id': cart_item.id,
                'price': cart_item.product.price,
                'product_id': cart_item.product.id,
            })
        context.update({
            'total_price': total_price,
            'cart_items': cart_items,
        })
        return context


class AddressView(LoginRequiredMixin, View):
    http_method_names = ['get', 'post', 'delete']
    
    def get(self, request, *args, **kwargs):
        addresses = Address.objects.filter(user=request.user)
        address_list = [
            {
                'id': address.pk,
                'zip_code': address.zip_code,
                'prefecture': address.prefecture,
                'address': address.address,
            }
            for address in addresses
        ]
        return render(request, 'stores/address.html', context={
            'addresses': address_list,
        })
        
    def validate_address_data(self, data):
        zip_code = data['zip_code']
        if not zip_code or not zip_code.isdigit() or len(zip_code) != 7:
            return JsonResponse(
                {'message': '郵便番号が不正です'},
                status=400
            )
        prefecture = data['prefecture']
        if not prefecture or len(prefecture) > 10:
            return JsonResponse(
                {'message': '都道府県が不正です'},
                status=400
            )
        address = data['address']
        if not address or len(address) > 200:
            return JsonResponse(
                {'message': '住所が不正です'},
                status=400
            )
    
    @method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse(
                {'message': 'リクエストが不正です'},
                status=400,
            )
        data = json.loads(request.body)
        validation_error = self.validate_address_data(data)
        if validation_error:
            return validation_error
        address = Address.objects.create(
            zip_code=data['zip_code'],
            prefecture=data['prefecture'],
            address=data['address'],
            user=request.user
        )
        return JsonResponse({
            'message': '住所を登録しました',
            'address_id': address.pk,
        })
    
    @method_decorator(csrf_protect)
    def delete(self, request, *args, **kwags):
        if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse(
                {'message': 'リクエストが不正です'},
                status=400,
            )
        data = json.loads(request.body)
        address_id = data['id']
        address = get_object_or_404(Address, id=address_id, user=request.user)
        address.delete()
        return JsonResponse({
            'message': '住所を削除しました'
        })
        


class OrderProductView(LoginRequiredMixin, FormView):
    template_name = 'stores/order.html'
    form_class = OrderForm
    success_url = reverse_lazy('accounts:home')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        address_id = self.request.GET.get('address_id')
        cart = get_object_or_404(Cart, user=self.request.user)
        address = get_object_or_404(Address, pk=address_id, user=self.request.user)
        if not cart.cart_items.exists(): # type: ignore
            raise Http404('カートが空です')
        total_price = 0
        cart_items = []
        for cart_item in cart.cart_items.select_related('product').all(): # type: ignore
            total_price += cart_item.quantity * cart_item.product.price
            picture = cart_item.product.pictures.first()
            picture = picture.picture if picture else None
            cart_items.append({
                'quantity': cart_item.quantity,
                'picture': picture,
                'name': cart_item.product.name,
                'id': cart_item.id,
                'price': cart_item.product.price,
            })
        context.update({
            'address': address,
            'cart': cart,
            'total_price': total_price,
            'cart_items': cart_items,
        })
        return context

    @transaction.atomic
    def form_valid(self, form):
        try:
            context = self.get_context_data()
            address = context['address']
            cart = context['cart']
            total_price = context['total_price']
            if not all([address, cart, total_price]):
                raise Http404('注文処理でエラーが発生しました')
            # 在庫チェック
            out_of_stock_items = []
            for item in cart.cart_items.select_related('product').all():
                if item.quantity > item.product.stock:
                    out_of_stock_items.append(item.product.name)
            if out_of_stock_items:
                raise Http404(
                    f'以下の商品の在庫が不足しています。{", ".join(out_of_stock_items)}'
                )
            order = Order.objects.create(
                user=self.request.user,
                address=address,
                total_price=total_price,
            )
            for item in cart.cart_items.all():
                product = item.product
                OrderItem.objects.create(
                    order=order, quantity=item.quantity, product=product
                )
                product.reduce_stock(item.quantity)
            cart.delete()
            messages.success(self.request, '注文処理が完了しました')
            return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, 'エラーが発生しました。')
            raise e
