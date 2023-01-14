from django.contrib import admin
from .models import (UserProfile, Category, Product,
                     Review, Purchase,
                     ProductCharacteristics, ProductPurchased)


admin.site.site_header = 'MEGANO'
admin.site.site_title = 'MEGANO'


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'payment_method']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'parent_category', 'name', 'image_src',
                    'short_image_name', 'big_image_src', 'has_subcategories']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'price', 'category', 'add1_image_src']


@admin.register(ProductCharacteristics)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'group', 'name', 'value']


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_profile', 'purchase_date', 'payment_method', 'delivery_type',
                    'delivery_state', 'payment_state']


@admin.register(ProductPurchased)
class ProductPurchasedAdmin(admin.ModelAdmin):
    list_display = ['id', 'purchase', 'product', 'price', 'amount']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_profile', 'product', 'rating', 'description']
