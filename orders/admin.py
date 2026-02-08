from django.contrib import admin
from .models import Order, Food

class OrderAdmin(admin.ModelAdmin):
    list_display = ('food_name', 'user', 'quantity', 'status', 'created_at')  # use 'food_name', not 'food'
    list_filter = ('status',)
    actions = ['confirm_orders', 'reject_orders']

    def confirm_orders(self, request, queryset):
        queryset.update(status='CONFIRMED')

    def reject_orders(self, request, queryset):
        queryset.update(status='REJECTED')

class FoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_available')
    list_editable = ('price', 'is_available')
    search_fields = ('name',)

# Register models safely
if not admin.site.is_registered(Order):
    admin.site.register(Order, OrderAdmin)

if not admin.site.is_registered(Food):
    admin.site.register(Food, FoodAdmin)
