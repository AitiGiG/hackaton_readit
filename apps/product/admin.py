from django.contrib import admin
from .models import Product, Busket, Review, Favorite

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'owner', 'price', 'quantity', 'available', 'created_at', 'updated_at')
    search_fields = ('title', 'category__name', 'owner__username')
    list_filter = ('category', 'owner', 'available')
    date_hierarchy = 'created_at'

@admin.register(Busket)
class BusketAdmin(admin.ModelAdmin):
    list_display = ('owner', 'product', 'quantity', 'created_timestamp')
    search_fields = ('owner__email', 'product__title')
    list_filter = ('created_timestamp',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('content', 'owner', 'created_at', 'product')
    search_fields = ('content', 'owner__username', 'product__title')
    list_filter = ('created_at', 'product')

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('product', 'owner')
    search_fields = ('product__title', 'owner__username')

