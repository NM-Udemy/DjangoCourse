from django.contrib import admin
from .models import (
    ProductTypes, Manufacturers, Products,
    ProductPictures
)


admin.site.register(
    [ProductTypes, Manufacturers, Products, ProductPictures]
)