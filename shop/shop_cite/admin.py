from django.contrib import admin
from .models import (UserProfile, Category, Product, Store,
                     Review, Delivery, Storage, Purchase, Basket)


admin.site.site_header = 'MEGANO'
admin.site.site_title = 'MEGANO'


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'payment_method']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'parent_category', 'name', 'image_src', 'short_image_name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'category']


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'address']


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ['id', 'store', 'address']


@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'store', 'price', 'amount']


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'store', 'price', 'amount', 'purchase_date', 'purchase_number']


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'store', 'price', 'amount']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'rating', 'description', 'store']
