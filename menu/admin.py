from django.contrib import admin
from .models import Category, Dish, Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'phone_number', 'delivery_type', 'total_price', 'created_at']
    list_filter = ['delivery_type', 'created_at']
    inlines = [OrderItemInline]

admin.site.register(Category)
admin.site.register(Dish)