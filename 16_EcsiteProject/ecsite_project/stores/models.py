from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ProductType(models.Model):
    name = models.CharField(max_length=1000)
    
    class Meta:
        db_table = 'product_type'
    
    def __str__(self):
        return self.name


class Manufacturer(models.Model):
    name = models.CharField(max_length=1000)
    
    class Meta:
        db_table = 'manufacturer'
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=1000)
    price = models.PositiveIntegerField()
    stock = models.PositiveIntegerField()
    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.CASCADE,
        related_name='products',
    )
    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete=models.CASCADE,
        related_name='products',
    )

    class Meta:
        db_table = 'product'
    
    def __str__(self):
        return self.name
    
    def reduce_stock(self, quantity):
        if self.stock < quantity:
            raise ValueError(f'{self.name}の在庫が不足しています')
        self.stock -= quantity
        self.save()
    
class ProductPicture(models.Model):
    picture = models.FileField(upload_to='product_pictures/')
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='pictures',
    )
    order = models.PositiveIntegerField()
    
    class Meta:
        db_table = 'product_picture'
        ordering = ['order']
    
    def __str__(self):
        return f'{self.product.name} - Picture {self.order}'


class Cart(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='cart'
    )
    
    class Meta:
        db_table = 'cart'
    
class CartItemManager(models.Manager):
    def save_item(self, product, quantity, cart):
        return self.create(
            quantity=quantity,
            product=product,
            cart=cart
        )    

class CartItem(models.Model):
    quantity = models.PositiveIntegerField()
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='cart_items',
    )
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='cart_items',
    )
    objects: CartItemManager = CartItemManager()
    
    class Meta:
        db_table = 'cart_item'
        unique_together = [['product', 'cart']]


class Address(models.Model):
    zip_code = models.CharField(max_length=8)
    prefecture = models.CharField(max_length=10)
    address = models.CharField(max_length=200)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='addresses'
    )
    
    class Meta:
        db_table = 'address'
        unique_together = [
            ['zip_code', 'prefecture', 'address', 'user']
        ]
    
    def __str__(self):
        return f'{self.zip_code} {self.prefecture} {self.address}'


class Order(models.Model):
    SHIPPING_STATUS_CHOICES = [
        ('waiting', '発送待ち'),
        ('shipped', '発送済み'),
        ('delivered', '配達完了'),
    ]
    total_price = models.PositiveIntegerField()
    address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='orders'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='orders'
    )
    shippng_status = models.CharField(
        max_length=20,
        choices=SHIPPING_STATUS_CHOICES,
        default='waiting',
    )
    
    class Meta:
        db_table = 'order'

class OrderItem(models.Model):
    quantity = models.PositiveIntegerField()
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='order_items'
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='order_items'
    )
    
    class Meta:
        db_table = 'order_item'
        unique_together = [['product', 'order']]
