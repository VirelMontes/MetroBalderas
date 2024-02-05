from django.contrib import admin
from .models import Product, CartItem

admin.site.register(Product)
# Register your models here.
admin.site.register(CartItem)