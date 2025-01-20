from django.contrib import admin
from .models import (
    ProductType, Manufacturer, Product, ProductPicture,
    Order, OrderItem
)

admin.site.register(
    [ProductType, Manufacturer, Product, ProductPicture,
     Order, OrderItem,]
)
