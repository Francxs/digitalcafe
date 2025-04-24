from django.contrib import admin
from .models import item, order, order_item

@admin.register(item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'item_price', 'stock_quantity')
    search_fields = ('item_name',)

@admin.register(order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_date', 'total_amount', 'payment_type')
    list_filter = ('payment_type', 'order_date')

@admin.register(order_item)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('item_id', 'order_id', 'quantity', 'line_total')
    
# ...existing admin registrations...