from django.contrib import admin
from .models import User, Category, Brand, Product, Order, OrderItem


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'role', 'is_staff']

admin.site.register(Brand)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'brand', 'price', 'stock']
    list_filter = ['category', 'brand', 'created_at']
    search_fields = ['name', 'description']

    fields = [
    'category',
    'brand',
    'name',
    'description',
    'price',
    'stock',
    'image',
    ]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['customer__username']
    inlines = [OrderItemInline]
